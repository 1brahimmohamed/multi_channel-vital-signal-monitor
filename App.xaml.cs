using System.Windows;
using System.Windows.Threading;
using SciChart.Charting.Visuals;
using SciChart.Examples.ExternalDependencies.Controls.ExceptionView;

namespace SciChartExport
{
    /// <summary>
    ///     Interaction logic for App.xaml
    /// </summary>
    public partial class App : Application
    {
        public App()
        {
            DispatcherUnhandledException += App_DispatcherUnhandledException;

            InitializeComponent();

            // TODO: Put your SciChart License Key here if needed  
            // Set this code once in App.xaml.cs or application startup
            SciChartSurface.SetRuntimeLicenseKey(
                "dVDD3irFeDgz/Xn0cezUEJ3nd/WSHe+llcidKEhF/99a/dkKP7ySawK3Jr6XQrWRN6zMBLLjUq8U+z1ciE0yY5ZSWpifNEIavurDBivF12iaaNYytHM1/nQfHsgA/Vw6iudQlQoy+QVZu5vaBGDdTKjpXpuuVZVzmdyFkfRqYNetX65z3a1IP0psZcVuq+7lYBKrro0SmWN7UBXFl2l7j11lD09LhLU7+1lR2vvR7MF6rdOPwHFR1HNPSK8iCPLnt3BSpGhdANn5rZ/BJmbmPQT4ofLEkM5ETVTzqMDONJwLJrLdhDUtW4XE+h2XTXd5XbCEMZyRMu7qBvn7a72SHJGEWukfibR1Kxcy/y/NluMvKhSuS+n6Z9eOFyTUziyBYlH004s3z7zp4wXnQqmSJl0qK1+4NoDJzi/8A4LiqqRQT8KAW4BlE/LM/i1sThC2k7vyR15TIQXSI0d1Q6MFB+YOE/vt9kF7sdyx1buoXhvF5yB+ImXJsrMxzCESGeB0JIgPzy+rG6sAJ6ksMmJW31j96Jd0f+kI5VbnNtNOrjhZEIQhTRtoOf5xMIHVi47yIOROGpA=");
        }

        private void App_DispatcherUnhandledException(object sender,
            DispatcherUnhandledExceptionEventArgs e)
        {
            var exceptionView = new ExceptionView(e.Exception)
            {
                WindowStartupLocation = WindowStartupLocation.CenterScreen
            };
            exceptionView.ShowDialog();

            e.Handled = true;
        }
    }
}