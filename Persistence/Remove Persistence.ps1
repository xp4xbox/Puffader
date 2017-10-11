If (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator"))
{
    $strFileName = (Get-Item -Path HKCU:\Software\Microsoft\Windows\CurrentVersion\Run).GetValue("winupdate")
    Get-Process | Where-Object {$_.Path -like $strFileName} | Stop-Process -Force

    $strFileDir = Split-Path $strFileName
    Remove-Item $strFileDir -Recurse -Force

    Remove-ItemProperty -path HKCU:\Software\Microsoft\Windows\CurrentVersion\Run -name winupdate
     

    Start-Process powershell.exe -Verb RunAs -ArgumentList ('-WindowStyle Hidden -noprofile -file "{0}" -elevated' -f ($myinvocation.MyCommand.Definition))
    exit
}

$strFileName = (Get-Item -Path HKLM:\Software\Microsoft\Windows\CurrentVersion\Run).GetValue("winupdate")

# kill the program
Get-Process | Where-Object {$_.Path -like $strFileName} | Stop-Process -Force

$strFileDir = Split-Path $strFileName

# delete folder
Remove-Item $strFileDir -Recurse -Force

# stop program from starting at startup
Remove-ItemProperty -path HKLM:\Software\Microsoft\Windows\CurrentVersion\Run -name winupdate

# restore text files to open with notepad
$WINDIR = "$env:WINDIR"
New-ItemProperty -path HKLM:\Software\Classes\txtfile\shell\open\command -name "(Default)" -PropertyType ExpandString -value "$WINDIR\NOTEPAD.EXE %1" -Force
