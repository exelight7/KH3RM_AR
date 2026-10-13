using Avalonia;
using Avalonia.Controls;
using Avalonia.Input;
using Avalonia.Interactivity;
using Avalonia.Media;
using Avalonia.Media.Imaging;
using Avalonia.Platform.Storage;
using Avalonia.Threading;
using System.IO;

namespace Kh3rmAr;
public partial class MainWindow : Window
{
    string? paks;
    string message = "";
    bool busy;
    readonly bool demo;
    public MainWindow()
    {
        InitializeComponent();
        var args = Program.Args;
        demo = args.Contains("--demo") || args.Contains("--render");
        Loc.Lang = args.Contains("en") || args.Contains("--english") ? "en" : "ar";
        if (demo) paks = OperatingSystem.IsWindows() ? @"C:\Steam\steamapps\common\KINGDOM HEARTS III" : "/home/deck/.local/share/Steam/steamapps/common/KINGDOM HEARTS III";
        else
        {
            // A restricted Steam library must not prevent choosing another folder manually.
            try { paks = Core.DetectAll().FirstOrDefault(); } catch (IOException) { }
            catch (UnauthorizedAccessException) { }
        }
        TickIfImagesInstalled();
        Apply();
        Closing += (_, e) => { if (busy) e.Cancel = true; };
        if (args.Length == 3 && args[0] == "--render")
            Opened += async (_, _) =>
            {
                await Task.Delay(1200);
                using var bitmap = new RenderTargetBitmap(new PixelSize((int)Bounds.Width, (int)Bounds.Height), new Vector(96, 96));
                bitmap.Render(this); bitmap.Save(args[2]); Close();
            };
    }
    string Text(string ar, string en) => Loc.Lang == "ar" ? ar : en;
    void Apply()
    {
        Panel.FlowDirection = Loc.Lang == "ar" ? FlowDirection.RightToLeft : FlowDirection.LeftToRight;
        HeroTitle.FlowDirection = HeroCaption.FlowDirection = Panel.FlowDirection;
        HeroTitle.Text = Text("حكايتك، بلغتك.", "Your story. Your language.");
        HeroCaption.Text = Text("عالم تعرفه. إحساس أقرب.", "A familiar world. A closer connection.");
        TitleText.Text = Text("رحلتك تبدأ\nبلغتك.", "Your journey.\nIn Arabic.");
        SubText.Text = Text("تعريب كينغدوم هارتس III + Re Mind", "Kingdom Hearts III + Re Mind, in Arabic.");
        FolderLabel.Text = Loc.Get("folder"); BrowseBtn.Content = Loc.Get("browse");
        InstallBtn.Content = Text("تثبيت التعريب  ←", "Install Arabic  →"); RemoveBtn.Content = Loc.Get("remove");
        LangBtn.Content = Loc.Get("lang"); LogCheck.Content = Text("حفظ السجل", "Save log");
        ImagesCheck.Content = Loc.Get("img_check"); RemoveImgBtn.Content = Loc.Get("rm_img");
        VerText.Text = "v" + Core.Version;
        DetectText.Text = Text("اكتشاف تلقائي لمكتبات Steam، أو اختر المجلد يدويًا.", "Detects Steam libraries, or select your game folder.");
        PlatformText.Text = OperatingSystem.IsLinux() ? "LINUX  /  STEAM + PROTON" : "WINDOWS  /  STEAM + EPIC";
        RefreshState();
        MsgText.Text = message;
    }
    void RefreshState()
    {
        PathText.Text = paks ?? "";
        InstallBtn.IsEnabled = !busy && paks != null; RemoveBtn.IsEnabled = !busy && paks != null;
        BrowseBtn.IsEnabled = LangBtn.IsEnabled = ImagesCheck.IsEnabled = !busy;
        RemoveImgBtn.IsVisible = false;
        if (paks == null) { StateText.Text = Loc.Get("st_nogame"); return; }
        try
        {
            var state = demo ? new Core.Status(Core.State.NotInstalled, 0) : Core.GetStatus(paks);
            StateText.Text = state.State switch { Core.State.Current => Loc.Get("st_cur", Core.Version), Core.State.OtherVersion => Loc.Get("st_old"), _ => Loc.Get("st_none") };
            var images = demo ? Core.State.NotInstalled : Core.GetStatus(paks, Core.Images).State;
            if (images != Core.State.NotInstalled) StateText.Text += Loc.Get(images == Core.State.Current ? "st_img_cur" : "st_img_old");
            if (state.OtherPaks > 0) StateText.Text += Loc.Get("st_other", state.OtherPaks);
            RemoveImgBtn.IsVisible = images != Core.State.NotInstalled; RemoveImgBtn.IsEnabled = !busy;
            Dot.Background = SolidColorBrush.Parse(state.State == Core.State.Current ? "#8CCEA9" : "#D8B975");
            RemoveBtn.IsEnabled = !busy && state.State != Core.State.NotInstalled;
        }
        catch (Exception) { StateText.Text = Loc.Get("error"); InstallBtn.IsEnabled = RemoveBtn.IsEnabled = false; }
    }
    // The images pack goes with Install / Remove only while its box is ticked; "remove images only" leaves the text pak.
    async Task Run(string action)
    {
        if (busy || demo || paks == null) return;
        var target = paks; var withImages = ImagesCheck.IsChecked == true;
        busy = true; BusyBar.IsVisible = true; message = ""; MsgText.Text = Text("جارٍ العمل…", "Working…"); RefreshState();
        try
        {
            var result = await Task.Run(() => action switch
            {
                "install" => Core.Install(target, withImages),
                "remove_images" => Core.Remove(target, null, Core.Images),
                _ => withImages ? Core.Remove(target, null, Core.All) : Core.Remove(target)
            });
            if (LogCheck.IsChecked == true) Core.Log($"{action}{(withImages && action != "remove_images" ? "+images" : "")}\t{result}\t{target}");
            message = result switch
            {
                Core.Result.Ok => Loc.Get(action switch { "install" => withImages ? "ok_inst_img" : "ok_inst", "remove_images" => "ok_rem_img", _ => "ok_rem" }),
                Core.Result.GameRunning => Loc.Get("running"), Core.Result.NoPaks => Loc.Get("badfolder"),
                Core.Result.Denied => Text("تعذر الوصول للمجلد. اختر مسارًا يمكنك الكتابة فيه.", "Folder is not writable. Check its permissions."),
                Core.Result.HashMismatch => Text("فشل التحقق. بقيت النسخة المثبتة كما هي.", "Verification failed. The installed copy was preserved."),
                _ => Loc.Get("error")
            };
            MsgText.Foreground = SolidColorBrush.Parse(result == Core.Result.Ok ? "#9AD7B2" : "#EDAD98");
        }
        finally { busy = false; BusyBar.IsVisible = false; RefreshState(); MsgText.Text = message; }
    }
    async void InstallClick(object? sender, RoutedEventArgs e) => await Run("install");
    async void RemoveClick(object? sender, RoutedEventArgs e) => await Run("remove");
    async void RemoveImgClick(object? sender, RoutedEventArgs e) => await Run("remove_images");
    /// <summary>The box starts off; it starts ticked only when this folder already holds our images pack.</summary>
    void TickIfImagesInstalled()
    {
        try { ImagesCheck.IsChecked = !demo && paks != null && Core.GetStatus(paks, Core.Images).State != Core.State.NotInstalled; }
        catch (Exception) { ImagesCheck.IsChecked = false; }
    }
    async void BrowseClick(object? sender, RoutedEventArgs e)
    {
        if (busy || demo) return;
        var choices = await StorageProvider.OpenFolderPickerAsync(new FolderPickerOpenOptions { Title = Loc.Get("folder"), AllowMultiple = false });
        if (choices.Count == 0) return;
        var candidate = Core.ResolvePaks(choices[0].TryGetLocalPath());
        if (candidate == null) { message = Loc.Get("badfolder"); MsgText.Text = message; return; }
        paks = candidate; message = ""; TickIfImagesInstalled(); Apply();
    }
    void LangClick(object? sender, RoutedEventArgs e) { Loc.Lang = Loc.Lang == "ar" ? "en" : "ar"; message = ""; Apply(); }
    void MinClick(object? sender, RoutedEventArgs e) => WindowState = WindowState.Minimized;
    void CloseClick(object? sender, RoutedEventArgs e) { if (!busy) Close(); }
    void TitleDrag(object? sender, PointerPressedEventArgs e) { if (!busy && e.GetCurrentPoint(this).Properties.IsLeftButtonPressed) BeginMoveDrag(e); }
}
