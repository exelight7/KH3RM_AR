using System.Diagnostics;
using System.IO;
using System.Reflection;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Animation;
using System.Windows.Media.Imaging;
using Ellipse = System.Windows.Shapes.Ellipse;
using System.Windows.Threading;

namespace Kh3rmAr;

public partial class MainWindow : Window
{
    string? paks;
    readonly bool demo;       // --render: fixed, game-independent content for the README screenshots
    readonly string? renderTo;
    string msg = "", msgKind = "";   // last message (key + colour kind) so a language switch re-translates it

    public MainWindow(string lang = "ar", string? renderPng = null)
    {
        InitializeComponent();
        Loc.Lang = lang;
        renderTo = renderPng;
        demo = renderPng != null;
        TitleIcon.Source = Art.RenderIcon(64);
        Icon = Art.RenderIcon(64);
        BuildSky();
        BuildSparkles();
        LoadArtSlot();
        paks = demo ? @"C:\Program Files (x86)\Steam\steamapps\common\KINGDOM HEARTS III\KINGDOM HEARTS III\Content\Paks" : Core.DetectAll().FirstOrDefault();
        Apply();
        if (demo) ContentRendered += (_, _) =>
        {
            var t = new DispatcherTimer { Interval = TimeSpan.FromMilliseconds(1600) };
            t.Tick += (_, _) => { t.Stop(); Art.SavePng(Root, renderTo!); Environment.Exit(0); };
            t.Start();
        };
    }

    // ---- decoration --------------------------------------------------------------------------------------
    void BuildSky()
    {
        var rnd = new Random(7);
        for (int i = 0; i < 120; i++)
        {
            double s = 0.8 + rnd.NextDouble() * 1.9;
            var star = new Ellipse
            {
                Width = s, Height = s, Opacity = 0.25 + rnd.NextDouble() * 0.6,
                Fill = new SolidColorBrush(rnd.Next(4) == 0 ? Color.FromRgb(255, 233, 170) : Color.FromRgb(214, 226, 255)),
            };
            Canvas.SetLeft(star, rnd.NextDouble() * 900); Canvas.SetTop(star, rnd.NextDouble() * 520);
            if (rnd.Next(3) == 0)
                star.BeginAnimation(OpacityProperty, new DoubleAnimation(0.1, 0.95, TimeSpan.FromSeconds(1.2 + rnd.NextDouble() * 2.5))
                { AutoReverse = true, RepeatBehavior = RepeatBehavior.Forever, BeginTime = TimeSpan.FromSeconds(rnd.NextDouble() * 2) });
            Sky.Children.Add(star);
        }
    }

    void BuildSparkles()
    {
        var geo = Geometry.Parse("M 0,-10 Q 1,-1 10,0 Q 1,1 0,10 Q -1,1 -10,0 Q -1,-1 0,-10 Z");
        var spots = new (double x, double y, double s)[] { (28, 40, 26), (222, 58, 20), (14, 168, 16), (238, 186, 24), (120, 8, 18), (186, 238, 14) };
        int k = 0;
        foreach (var (x, y, s) in spots)
        {
            var sc = new ScaleTransform(0.4, 0.4);
            var p = new System.Windows.Shapes.Path
            {
                Data = geo, Width = s, Height = s, Stretch = Stretch.Fill, Fill = new SolidColorBrush(Color.FromRgb(255, 226, 140)),
                RenderTransformOrigin = new Point(0.5, 0.5), RenderTransform = sc, Opacity = 0.2,
                Effect = new System.Windows.Media.Effects.DropShadowEffect { Color = Color.FromRgb(255, 211, 107), BlurRadius = 10, ShadowDepth = 0 },
            };
            Canvas.SetLeft(p, x); Canvas.SetTop(p, y);
            var dur = TimeSpan.FromSeconds(1.6 + 0.3 * k); var begin = TimeSpan.FromSeconds(0.4 * k++);
            p.BeginAnimation(OpacityProperty, new DoubleAnimation(0.1, 1, dur) { AutoReverse = true, RepeatBehavior = RepeatBehavior.Forever, BeginTime = begin });
            sc.BeginAnimation(ScaleTransform.ScaleXProperty, new DoubleAnimation(0.4, 1.15, dur) { AutoReverse = true, RepeatBehavior = RepeatBehavior.Forever, BeginTime = begin });
            sc.BeginAnimation(ScaleTransform.ScaleYProperty, new DoubleAnimation(0.4, 1.15, dur) { AutoReverse = true, RepeatBehavior = RepeatBehavior.Forever, BeginTime = begin });
            Sparkles.Children.Add(p);
        }
    }

    /// <summary>Optional user-supplied art (art\background.png + art\CREDIT.txt, embedded at build time).</summary>
    void LoadArtSlot()
    {
        var asm = Assembly.GetExecutingAssembly();
        using var bg = asm.GetManifestResourceStream("art.bg");
        if (bg == null) return;
        var bmp = new BitmapImage();
        bmp.BeginInit(); bmp.CacheOption = BitmapCacheOption.OnLoad; bmp.StreamSource = bg; bmp.EndInit(); bmp.Freeze();
        BgImage.Source = bmp; BgImage.Visibility = Visibility.Visible;
        using var cr = asm.GetManifestResourceStream("art.credit");
        if (cr != null) CreditText.Text = new StreamReader(cr).ReadToEnd().Trim();
    }

    // ---- text / state ------------------------------------------------------------------------------------
    void Apply()
    {
        Panel.FlowDirection = Loc.Lang == "ar" ? FlowDirection.RightToLeft : FlowDirection.LeftToRight;
        TitleText.Text = Loc.Get("title"); SubText.Text = Loc.Get("sub"); FolderLabel.Text = Loc.Get("folder");
        BrowseBtn.Content = Loc.Get("browse"); InstallBtn.Content = Loc.Get("install"); RemoveBtn.Content = Loc.Get("remove");
        LogCheck.Content = Loc.Get("savelog"); LangBtn.Content = Loc.Get("lang"); FootText.Text = Loc.Get("foot");
        VerText.Text = Loc.Get("ver", Core.Version);
        RefreshState();
        ShowMsg(msg, msgKind);
    }

    void RefreshState()
    {
        PathText.Text = paks ?? Loc.Get("notfound");
        InstallBtn.IsEnabled = RemoveBtn.IsEnabled = paks != null;
        if (paks == null) { StateText.Text = Loc.Get("st_nogame"); Dot.Fill = Brush("#8896C8"); return; }
        if (demo) { StateText.Text = Loc.Get("st_none"); Dot.Fill = Brush("#8896C8"); return; }
        var st = Core.GetStatus(paks);
        (StateText.Text, Dot.Fill) = st.State switch
        {
            Core.State.Current => (Loc.Get("st_cur", Core.Version), Brush("#7CE0A3")),
            Core.State.OtherVersion => (Loc.Get("st_old"), Brush("#F6C65B")),
            _ => (Loc.Get("st_none"), Brush("#8896C8")),
        };
        if (st.OtherPaks > 0) StateText.Text += Loc.Get("st_other", st.OtherPaks);
    }

    static SolidColorBrush Brush(string hex) => new((Color)ColorConverter.ConvertFromString(hex));

    void ShowMsg(string key, string kind)
    {
        msg = key; msgKind = kind;
        MsgText.Text = key == "" ? "" : Loc.Get(key);
        MsgText.Foreground = Brush(kind == "ok" ? "#7CE0A3" : kind == "err" ? "#FF9A9A" : "#F6C65B");
    }

    // ---- actions -----------------------------------------------------------------------------------------
    void Done(Core.Result r, string okKey)
    {
        if (LogCheck.IsChecked == true) Core.Log($"{okKey}\t{r}\t{paks}");
        switch (r)
        {
            case Core.Result.Ok: ShowMsg(okKey, "ok"); break;
            case Core.Result.GameRunning: ShowMsg("running", "err"); break;
            case Core.Result.NoPaks: ShowMsg("badfolder", "err"); break;
            case Core.Result.HashMismatch: ShowMsg("badhash", "err"); break;
            case Core.Result.Denied: AskAdmin(); break;
            default: ShowMsg("error", "err"); break;
        }
        RefreshState();
    }

    void AskAdmin()
    {
        ShowMsg("denied", "err");
        var opt = Loc.Lang == "ar" ? MessageBoxOptions.RightAlign | MessageBoxOptions.RtlReading : MessageBoxOptions.None;
        if (MessageBox.Show(Loc.Get("denied"), "KH3RM_AR", MessageBoxButton.YesNo, MessageBoxImage.Question, MessageBoxResult.Yes, opt) != MessageBoxResult.Yes) return;
        try { Process.Start(new ProcessStartInfo(Environment.ProcessPath!) { UseShellExecute = true, Verb = "runas" }); Application.Current.Shutdown(); }
        catch (Exception) { /* UAC cancelled */ }
    }

    void InstallClick(object s, RoutedEventArgs e) { if (paks != null) Done(Core.Install(paks), "ok_inst"); }
    void RemoveClick(object s, RoutedEventArgs e) { if (paks != null) Done(Core.Remove(paks), "ok_rem"); }

    void BrowseClick(object s, RoutedEventArgs e)
    {
        var dlg = new Microsoft.Win32.OpenFolderDialog { Title = Loc.Get("folder") };
        if (dlg.ShowDialog(this) != true) return;
        var p = Core.ResolvePaks(dlg.FolderName);
        if (p == null) { ShowMsg("badfolder", "err"); return; }
        paks = p; ShowMsg("", ""); RefreshState();
    }

    void LangClick(object s, RoutedEventArgs e) { Loc.Lang = Loc.Lang == "ar" ? "en" : "ar"; Apply(); }
    void MinClick(object s, RoutedEventArgs e) => WindowState = WindowState.Minimized;
    void CloseClick(object s, RoutedEventArgs e) => Close();
    void TitleDrag(object s, MouseButtonEventArgs e) { if (e.ButtonState == MouseButtonState.Pressed) DragMove(); }
}
