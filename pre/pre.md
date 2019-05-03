# Information Gathering Cheatsheet

## Unknown Services

```
amap -d <IP> <Port>
```

## HTTP


### DAV

```
davtest -url <URL>
cadaver <URL>
```

### HTTP Options

Especially helpful in case of open directory listings - maybe PUT is possible

```
curl -i -X OPTIONS <URL>/dir
```

## SMB

### Common Tools and Commands

Use nbtscan from [here](http://www.unixwiz.net/tools/nbtscan.html) instead of the version in Kali because of reasons.

```
enum4linux -a 10.11.1.136
nmblookup -A 10.11.1.136
smbclient //MOUNT/share -I 10.11.1.136 -N
smbclient -L //10.11.1.136
rpcclient -U "" 10.11.1.136
mount //10.11.1.5/share /mnt # Mount open shares
```

### Checking SMB Vulnerabilities

```
bash -c "nmap -p 139,445 --script=smb-vuln* 10.11.1.136"
```

### Check For Common SMB Issues

Null Sessions:
```
crackmapexec smb 10.11.1.136 -u '' -p '' --shares
```

RID Brute Forcing:

```
crackmapexec smb 10.11.1.136 -u '' -p '' --rid-brute
```

Code Execution:

```
crackmapexec smb 10.11.1.136 -u '' -p '' -x 'whoami'
```

Read SAM/LSA:

```
crackmapexec smb 10.11.1.136 -u '' -p '' --sam

crackmapexec smb 10.11.1.136 -u '' -p '' --lsa
```

Download Whole Share
```
smbclient '\\server\share'
mask ""
recurse ON
prompt OFF
cd 'path\to\remote\dir'
lcd '/path/to/download/to/'
mget *
```

### Determine Remote SMB Version

```
ngrep -i -d tap0 's.?a.?m.?b.?a.*[[:digit:]]'
smbclient -L //<IP>
```

## Coldfusion

Check [this](https://nets.ec/Coldfusion_hacking).

## Sensitive Windows Files

```
%windir%\repair\sam
%windir%\System32\config\RegBack\SAM
%windir%\repair\system
%windir%\repair\software
%windir%\repair\security
%windir%\debug\NetSetup.log (AD domain name, DC name, internal IP, DA account)
%windir%\iis6.log (5,6 or 7)
%windir%\system32\logfiles\httperr\httperr1.log
C:\sysprep.inf
C:\sysprep\sysprep.inf
C:\sysprep\sysprep.xml
%windir%\Panther\Unattended.xml
C:\inetpub\wwwroot\Web.config
%windir%\system32\config\AppEvent.Evt (Application log)
%windir%\system32\config\SecEvent.Evt (Security log)
%windir%\system32\config\default.sav
%windir%\system32\config\security.sav
%windir%\system32\config\software.sav
%windir%\system32\config\system.sav
%windir%\system32\inetsrv\config\applicationHost.config
%windir%\system32\inetsrv\config\schema\ASPNET_schema.xml
%windir%\System32\drivers\etc\hosts (dns entries)
%windir%\System32\drivers\etc\networks (network settings)
%windir%\system32\config\SAM (only really useful if you have access to the files while the machine is off)
```

## DNS

### Zone Transfer

```
host -t axfr <domain> <dns server ip>
dig axfr @10.10.10.123 # For root zone
dig axfr friendzoneportal.red @10.10.10.123 # For specific zone
```

### Enumeration

#### NSLookup

```
nslookup <<< INPUT
SERVER 10.10.10.123
127.0.0.1
10.10.10.123
INPUT
```

#### DNSRecon

```
dnsrecon -r 127.0.0.0/24 -n 10.10.10.123
dnsrecon -r 127.0.1.0/24 -n 10.10.10.123
dnsrecon -r 10.10.10.0/24 -n 10.10.10.123
```

## Resources

[Penetration Testing Tools Cheat Sheet](https://highon.coffee/blog/penetration-testing-tools-cheat-sheet/)
[HighOn.Coffee Nmap Cheatsheet](https://highon.coffee/blog/nmap-cheat-sheet/)
