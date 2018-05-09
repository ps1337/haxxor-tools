# Port Forwarding

## SSH

```
ssh -L <Port on attacker machine>:localhost:<Port on victim> user@host
```

## Socat

Forward local SSH server to public port 1337
```
socat tcp-listen:1337,reuseaddr,fork tcp:localhost:22
```

# Resources

- [A Red Teamer's guide to pivoting](https://artkond.com/2017/03/23/pivoting-guide/)
