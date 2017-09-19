$strFileName = (Get-Item -Path HKCU:\Software\Microsoft\Windows\CurrentVersion\Run).GetValue("winupdate")
Remove-Item $strFileName -Force

Remove-ItemProperty -path HKCU:\Software\Microsoft\Windows\CurrentVersion\Run -name winupdate
