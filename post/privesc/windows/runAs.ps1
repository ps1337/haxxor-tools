$username = 'yolo'
$password = 'yoloishere'

$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential $username, $securePassword
Start-Process cmd.exe -Credential $credential

# perhaps type "exit" after spawning cmd.exe if the session is borked somehow :)