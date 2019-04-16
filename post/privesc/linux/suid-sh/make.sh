#!/bin/bash

# need gcc-multilib

gcc -m32 -Wl,--hash-style=both -o suid suid.c


