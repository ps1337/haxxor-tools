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

## Writeable `/etc/sudoers`
Append:
```
<username>      ALL = NOPASSWD: ALL
```
