using System.IO;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using System.Windows.Media.Imaging;

namespace Kh3rmAr;

public partial class App : Application
{
    // KH3RM_AR_Setup.exe                       normal start
    //   --selftest <out.txt>                   self tests on temp folders (exit 0 = all pass)
    //   --render ar|en <out.png>               render the window with demo content to a PNG, then exit
    //   --icon <out.ico>                       write the app icon (heart + keyhole)
    protected override void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);
        var a = e.Args;
        if (a.Length == 2 && a[0] == "--selftest") Environment.Exit(SelfTest.Run(a[1]));
        if (a.Length == 2 && a[0] == "--icon") { Art.WriteIco(a[1]); Environment.Exit(0); }
        if (a.Length == 3 && a[0] == "--render") { new MainWindow(a[1], a[2]).Show(); return; }
        new MainWindow().Show();
    }
}

/// <summary>Draws the app icon / PNG captures from the XAML emblem.</summary>
public static class Art
{
    public static BitmapSource RenderIcon(int size)
    {
        var box = new Border
        {
            Width = size, Height = size, CornerRadius = new CornerRadius(size * 0.22), Padding = new Thickness(size * 0.06),
            Background = new LinearGradientBrush(Color.FromRgb(5, 10, 34), Color.FromRgb(27, 45, 117), 60),
            Child = new Emblem(),
        };
        return Capture(box, size, size);
    }

    static BitmapSource Capture(FrameworkElement el, int w, int h)
    {
        el.Measure(new Size(w, h)); el.Arrange(new Rect(0, 0, w, h)); el.UpdateLayout();
        var rtb = new RenderTargetBitmap(w, h, 96, 96, PixelFormats.Pbgra32);
        rtb.Render(el);
        rtb.Freeze();
        return rtb;
    }

    public static void SavePng(FrameworkElement el, string path)
    {
        var rtb = new RenderTargetBitmap((int)el.ActualWidth, (int)el.ActualHeight, 96, 96, PixelFormats.Pbgra32);
        rtb.Render(el);
        var enc = new PngBitmapEncoder(); enc.Frames.Add(BitmapFrame.Create(rtb));
        using var f = File.Create(path); enc.Save(f);
    }

    /// <summary>ICO with PNG-compressed images (valid since Windows Vista).</summary>
    public static void WriteIco(string path)
    {
        var sizes = new[] { 256, 64, 48, 32, 16 };
        var pngs = sizes.Select(s =>
        {
            var enc = new PngBitmapEncoder(); enc.Frames.Add(BitmapFrame.Create(RenderIcon(s)));
            using var ms = new MemoryStream(); enc.Save(ms); return ms.ToArray();
        }).ToList();
        using var w = new BinaryWriter(File.Create(path));
        w.Write((short)0); w.Write((short)1); w.Write((short)sizes.Length);
        int off = 6 + 16 * sizes.Length;
        for (int i = 0; i < sizes.Length; i++)
        {
            w.Write((byte)(sizes[i] == 256 ? 0 : sizes[i])); w.Write((byte)(sizes[i] == 256 ? 0 : sizes[i]));
            w.Write((byte)0); w.Write((byte)0); w.Write((short)1); w.Write((short)32);
            w.Write(pngs[i].Length); w.Write(off); off += pngs[i].Length;
        }
        foreach (var p in pngs) w.Write(p);
    }
}
