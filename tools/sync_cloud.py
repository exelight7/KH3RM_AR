r"""Cloud sync (run through tools\sync_cloud.bat). Never force-pushes; only cloud_repo\ (private KH3RM_AR_work, branch main) is pushed.
 (a) git pull --ff-only in cloud_repo\ (the user has merged the cloud pull requests on GitHub);
     take the cloud corrections that are new (review/corrections/applied/cloud/*.tsv of cloud_repo not yet applied here) and the cloud-owned
     notes (review/UNSURE_CLOUD.md, review/CLOUD_BUGS.md, state/CLOUD_PROGRESS.md); apply them with tools/apply_corrections.py
     (refuses everything if any old_AR differs = the row changed locally after the export: reported, nothing overwritten);
     report translation rows that differ between cloud_repo/ and the private project for any other reason; validate must give 0 ERR.
 (b) regenerate cloud_repo\ (make_cloud), cloud_secret_check + cloud_check, commit "sync: <date>", push.
Usage: python -I tools\sync_cloud.py [--no-push]"""
import datetime, filecmp, os, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import apply_corrections, cloud_secret_check, make_cloud, validate
from tsvlib import ROOT, read_tsv

CLOUD = make_cloud.DST
OWNED = ['review/UNSURE_CLOUD.md', 'review/CLOUD_BUGS.md', 'state/CLOUD_PROGRESS.md']
APPLIED = ['review', 'corrections', 'applied', 'cloud']


def git(*a, check=True):
    p = subprocess.run(['git', '-C', CLOUD, *a], capture_output=True, text=True, encoding='utf-8')
    if check and p.returncode:
        raise SystemExit(f'git {" ".join(a)} failed:\n{p.stdout}{p.stderr}')
    return p.stdout.strip()


def tsv_diff():
    """ids whose row differs between cloud_repo/ and the private project (translation TSVs)"""
    out = []
    for cat in sorted(os.listdir(os.path.join(ROOT, 'translation'))):
        d = os.path.join(ROOT, 'translation', cat)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            c = os.path.join(CLOUD, 'translation', cat, fn)
            if fn.endswith('.tsv') and os.path.exists(c) and not filecmp.cmp(os.path.join(d, fn), c, shallow=False):
                a, b = {r[0]: r for r in read_tsv(os.path.join(d, fn))}, {r[0]: r for r in read_tsv(c)}
                out += [i for i in a if a[i] != b.get(i)]
    return out


def main():
    push = '--no-push' not in sys.argv
    if not os.path.isdir(os.path.join(CLOUD, '.git')):
        raise SystemExit('sync_cloud: cloud_repo\\ is not a git repo (run the CLOUD-PREP setup first)')
    if git('status', '--porcelain'):
        raise SystemExit('sync_cloud: cloud_repo has uncommitted changes; commit or discard them first')
    git('checkout', 'main')
    print('pull:', git('pull', '--ff-only') or 'ok')
    # (a) new cloud corrections
    src, dst = os.path.join(CLOUD, *APPLIED), os.path.join(ROOT, *APPLIED)
    new = sorted(f for f in os.listdir(src) if f.endswith('.tsv') and not os.path.exists(os.path.join(dst, f))) if os.path.isdir(src) else []
    inbox = os.path.join(ROOT, 'review', 'corrections', 'cloud')
    os.makedirs(inbox, exist_ok=True)
    for f in new:
        shutil.copyfile(os.path.join(src, f), os.path.join(inbox, f))
    print(f'new cloud correction files: {len(new)} {new}')
    for rel in OWNED:
        s, d = os.path.join(CLOUD, *rel.split('/')), os.path.join(ROOT, *rel.split('/'))
        if os.path.exists(s) and (not os.path.exists(d) or not filecmp.cmp(s, d, shallow=False)):
            shutil.copyfile(s, d)
            print('updated from cloud:', rel)
    try:
        print(f'apply_corrections: {apply_corrections.apply()} applied')
    except SystemExit as e:
        print(e)
        print('sync_cloud STOP: nothing applied. Rows changed locally after the export? Resolve the lines above, then re-run.')
        return 1
    extra = tsv_diff()
    if extra:
        print(f'REPORT: {len(extra)} translation rows differ between cloud_repo/ and the private project and are NOT explained by cloud '
              f'corrections (cloud branch edited a TSV by hand, or local changes after export). Private version is kept. First ids: {extra[:15]}')
    flags = validate.validate_all()
    err = [i for i, f in flags.items() if validate.ERR & set(f)]
    print(f'validate: {len(err)} ERR rows')
    if err:
        print('sync_cloud STOP: validate has errors:', err[:20])
        return 1
    # (b) regenerate and push
    make_cloud.main()
    p = subprocess.run([sys.executable, '-I', os.path.join(CLOUD, 'tools', 'cloud_check.py')], cwd=CLOUD)
    if p.returncode:
        print('sync_cloud STOP: cloud_check FAIL in cloud_repo')
        return 1
    git('add', '-A')
    if git('status', '--porcelain'):
        git('commit', '-q', '-m', f'sync: {datetime.date.today()}')
        print('committed in cloud_repo')
    if push:
        print('push:', git('push', 'origin', 'main') or 'ok')
    print('sync_cloud OK. Commit the private project now (refresh.bat, secret_check).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
