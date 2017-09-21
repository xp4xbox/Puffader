$strFileName = (Get-Item -Path HKCU:\Software\Microsoft\Windows\CurrentVersion\Run).GetValue("winupdate")

# kill and delete program
Get-Process | Where-Object {$_.Path -like $strFileName} | Stop-Process -Force
Remove-Item $strFileName -Force

Remove-ItemProperty -path HKCU:\Software\Microsoft\Windows\CurrentVersion\Run -name winupdate
