"""Cloud check (run after every page and by GitHub Actions): translation integrity + validate (0 ERR) + unit tests + secret scan.
Prints PASS/FAIL per step and a final line; exit code 0 only if everything passes. Works on Linux and Windows (ASCII output).
Usage: python -I tools/cloud_check.py"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
TESTS = ['test_validate.py', 'test_corrections.py', 'test_shaper.py', 'test_cloud_secret_check.py']


def step(name, ok, detail=''):
    print(f'{"PASS" if ok else "FAIL"}  {name}' + (f'  ({detail})' if detail else ''))
    return ok


def run_py(*a):
    p = subprocess.run([sys.executable, '-I', *a], capture_output=True, text=True, encoding='utf-8', errors='replace')
    return p.returncode == 0, (p.stdout + p.stderr).strip().splitlines()[-1:] or ['']


def main():
    import cloud_secret_check
    import validate
    from tsvlib import ROOT
    res = []
    ok, tail = run_py(os.path.join(HERE, 'merge_translation.py'), '--check')
    res.append(step('translation merge check (EN unchanged)', ok, tail[0]))
    flags = validate.validate_all()
    err = sum(1 for f in flags.values() if validate.ERR & set(f))
    warn = sum(1 for f in flags.values() if not validate.ERR & set(f))
    res.append(step('validate', err == 0, f'{err} ERR rows, {warn} WARN-only rows'))
    if err:
        for i, f in [(i, f) for i, f in flags.items() if validate.ERR & set(f)][:20]:
            print(f'      {i}: {" ".join(f)}')
    for t in TESTS:
        ok, tail = run_py(os.path.join(HERE, t))
        res.append(step(t, ok, tail[0] if not ok else ''))
    bad = cloud_secret_check.run(ROOT)
    res.append(step('secret scan', not bad, '; '.join(bad[:5])))
    print('cloud_check', 'PASS' if all(res) else 'FAIL')
    return 0 if all(res) else 1


if __name__ == '__main__':
    sys.exit(main())
