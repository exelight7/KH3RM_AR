using Avalonia;
namespace Kh3rmAr;
internal static class Program
{
    public static string[] Args = Array.Empty<string>();
    [STAThread]
    public static void Main(string[] args)
    {
        Args = args;
        if (args.Length == 2 && args[0] == "--selftest") { Environment.Exit(SelfTest.Run(args[1])); return; }
        AppBuilder.Configure<App>().UsePlatformDetect().LogToTrace().StartWithClassicDesktopLifetime(args);
    }
}
