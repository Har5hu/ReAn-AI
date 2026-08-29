Add-Type -AssemblyName PresentationCore
Add-Type -AssemblyName WindowsBase

$clip = 'C:\Users\harsh\AppData\Local\Packages\Microsoft.ScreenSketch_8wekyb3d8bbwe\TempState\Recordings\20260810-1039-39.7415294.mp4'
$outputFolder = 'C:\Users\harsh\OneDrive\Desktop\DS Project\ATS checker v2\recording-frames'
New-Item -ItemType Directory -Force -Path $outputFolder | Out-Null

function Wait-ForDispatcher([int]$milliseconds) {
  $frame = New-Object System.Windows.Threading.DispatcherFrame
  $timer = New-Object System.Windows.Threading.DispatcherTimer
  $timer.Interval = [TimeSpan]::FromMilliseconds($milliseconds)
  $timer.Add_Tick({ param($timerSender, $timerEventArgs) $timerSender.Stop(); $frame.Continue = $false })
  $timer.Start()
  [System.Windows.Threading.Dispatcher]::PushFrame($frame)
}

$player = New-Object System.Windows.Media.MediaPlayer
$script:opened = $false
$player.Add_MediaOpened({ $script:opened = $true })
$player.Open([Uri]$clip)

for ($attempt = 0; $attempt -lt 100 -and -not $script:opened; $attempt++) { Wait-ForDispatcher 100 }
if (-not $script:opened) { throw 'Unable to open the recording.' }

foreach ($second in @(4, 20, 38, 56, 70)) {
  $player.Position = [TimeSpan]::FromSeconds($second)
  $player.Play()
  Wait-ForDispatcher 900
  $player.Pause()

  $drawing = New-Object System.Windows.Media.VideoDrawing
  $drawing.Player = $player
  $drawing.Rect = New-Object System.Windows.Rect(0, 0, 1280, 720)
  $visual = New-Object System.Windows.Media.DrawingVisual
  $context = $visual.RenderOpen()
  $context.DrawDrawing($drawing)
  $context.Close()
  $bitmap = New-Object System.Windows.Media.Imaging.RenderTargetBitmap(1280, 720, 96, 96, [System.Windows.Media.PixelFormats]::Pbgra32)
  $bitmap.Render($visual)
  $encoder = New-Object System.Windows.Media.Imaging.PngBitmapEncoder
  $encoder.Frames.Add([System.Windows.Media.Imaging.BitmapFrame]::Create($bitmap))
  $stream = [System.IO.File]::Open((Join-Path $outputFolder "frame-$second.png"), [System.IO.FileMode]::Create)
  $encoder.Save($stream)
  $stream.Close()
}

$player.Close()
