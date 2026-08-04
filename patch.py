#!/usr/bin/env python3

FLASH = "flash_test.bin"
TEST  = "test.bin"
OUT   = "patched.bin"
OFFSET = 0xEA00
flash = bytearray(open(FLASH, "rb").read())
test  = open(TEST, "rb").read()

flash[OFFSET:OFFSET+len(test)] = test

open(OUT, "wb").write(flash)

print(f"wrote to: {OUT}")
print(f"offset: 0x{OFFSET:04X}")
print(f"size: {len(test)} bytes")
