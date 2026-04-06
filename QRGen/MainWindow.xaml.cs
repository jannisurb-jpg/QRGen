using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Diagnostics;
using System.Windows.Media.Media3D;
using System.Threading.Tasks;

namespace QRGen
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private void Grid_MouseDown(object sender, MouseButtonEventArgs e)
        {
            if (e.ChangedButton == MouseButton.Left)
            {
                DragMove();
            }
        }

        private void Close_window(object sender, RoutedEventArgs e)
        {
            Application.Current.Shutdown();
        }

       private void Minimize_window(object sender, RoutedEventArgs e)
        {
            WindowState = WindowState.Minimized;
        }

        private async void CreateQR(object sender, RoutedEventArgs e)
        {
            string input = InputBox.Text;

            if(string.IsNullOrWhiteSpace(input))
            {
                return;
            }

            await GenerateQRCode(input);
        }

        private async Task GenerateQRCode(string data)
        {
            string scriptPath = "generator.py";
            string outputPath = "QRGen.png";

            await Task.Run(() =>
            {
                Process process = new Process();
                process.StartInfo.FileName = "python";
                process.StartInfo.Arguments = $"{scriptPath} \"{data}\" \"{outputPath}\"";
                process.StartInfo.UseShellExecute = false;
                process.StartInfo.RedirectStandardOutput = true;
                process.StartInfo.RedirectStandardError = true;
                process.StartInfo.CreateNoWindow = true;

                process.Start();
                process.WaitForExit();
            });

            Dispatcher.Invoke(() =>
            {
                var bitmap = new BitmapImage();
                bitmap.BeginInit();
                bitmap.UriSource = new Uri(System.IO.Path.GetFullPath(outputPath));
                bitmap.CacheOption = BitmapCacheOption.OnLoad; // loads fully then releases file
                bitmap.EndInit();
                QRImage.Source = bitmap;
            });
        }
    }
}