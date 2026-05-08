Add-Type -AssemblyName System.Drawing

function New-RadarLogo([int]$size) {
  $bmp = New-Object System.Drawing.Bitmap($size, $size, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
  $g.Clear([System.Drawing.Color]::Transparent)

  # Scale factor: SVG is 100x100
  $scale = $size / 100.0
  $green = [System.Drawing.Color]::FromArgb(255, 78, 207, 122)
  $green60 = [System.Drawing.Color]::FromArgb(153, 78, 207, 122)
  $green35 = [System.Drawing.Color]::FromArgb(89, 78, 207, 122)

  function S([double]$v) { return $v * $scale }
  function Pen([System.Drawing.Color]$c, [double]$w) {
    $p = New-Object System.Drawing.Pen($c, [float](S $w))
    $p.StartCap = [System.Drawing.Drawing2D.LineCap]::Round
    $p.EndCap = [System.Drawing.Drawing2D.LineCap]::Round
    return $p
  }

  # Outer circle r=44 stroke 6
  $p1 = Pen $green 6
  $g.DrawEllipse($p1, [float](S(50-44)), [float](S(50-44)), [float](S(88)), [float](S(88)))
  $p1.Dispose()

  # Middle circle r=29 stroke 4 opacity .6
  $p2 = Pen $green60 4
  $g.DrawEllipse($p2, [float](S(50-29)), [float](S(50-29)), [float](S(58)), [float](S(58)))
  $p2.Dispose()

  # Inner circle r=14 stroke 3 opacity .35
  $p3 = Pen $green35 3
  $g.DrawEllipse($p3, [float](S(50-14)), [float](S(50-14)), [float](S(28)), [float](S(28)))
  $p3.Dispose()

  # Sweep line from (50,50) to (84,18) stroke 5
  $p4 = Pen $green 5
  $g.DrawLine($p4, [float](S 50), [float](S 50), [float](S 84), [float](S 18))
  $p4.Dispose()

  # Center dot r=5 filled
  $brush = New-Object System.Drawing.SolidBrush($green)
  $g.FillEllipse($brush, [float](S(50-5)), [float](S(50-5)), [float](S(10)), [float](S(10)))
  $brush.Dispose()

  $g.Dispose()
  return $bmp
}

# Generate PNGs
$sizes = @{ 'favicon-16x16.png' = 16; 'favicon-32x32.png' = 32; 'apple-touch-icon.png' = 180; 'android-chrome-192x192.png' = 192; 'android-chrome-512x512.png' = 512 }
foreach ($file in $sizes.Keys) {
  $bmp = New-RadarLogo $sizes[$file]
  $path = "C:\Users\hugod\peptideradar\$file"
  $bmp.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
  $bmp.Dispose()
  Write-Output "wrote $file ($($sizes[$file])x$($sizes[$file]))"
}

# Build multi-res ICO with 16, 32, 48 PNGs embedded
$icoSizes = @(16, 32, 48)
$pngBytes = @()
foreach ($s in $icoSizes) {
  $bmp = New-RadarLogo $s
  $ms = New-Object System.IO.MemoryStream
  $bmp.Save($ms, [System.Drawing.Imaging.ImageFormat]::Png)
  $pngBytes += ,($ms.ToArray())
  $bmp.Dispose()
  $ms.Dispose()
}

$icoPath = 'C:\Users\hugod\peptideradar\favicon.ico'
$fs = [System.IO.File]::Create($icoPath)
$bw = New-Object System.IO.BinaryWriter($fs)

# ICONDIR header
$bw.Write([uint16]0)        # reserved
$bw.Write([uint16]1)        # type: 1 = ICO
$bw.Write([uint16]$icoSizes.Count)  # count

# ICONDIRENTRY for each
$offset = 6 + (16 * $icoSizes.Count)
for ($i = 0; $i -lt $icoSizes.Count; $i++) {
  $sz = $icoSizes[$i]
  $bytes = $pngBytes[$i]
  $w = if ($sz -ge 256) { 0 } else { $sz }
  $h = if ($sz -ge 256) { 0 } else { $sz }
  $bw.Write([byte]$w)        # width (0 means 256)
  $bw.Write([byte]$h)        # height
  $bw.Write([byte]0)         # color count (0 = >256 colors)
  $bw.Write([byte]0)         # reserved
  $bw.Write([uint16]1)       # color planes
  $bw.Write([uint16]32)      # bits per pixel
  $bw.Write([uint32]$bytes.Length)  # image size
  $bw.Write([uint32]$offset) # offset
  $offset += $bytes.Length
}

# Image data
foreach ($bytes in $pngBytes) {
  $bw.Write($bytes)
}

$bw.Close()
$fs.Close()
Write-Output "wrote favicon.ico ($icoSizes -join ' + ' )"
