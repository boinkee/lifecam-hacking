#!/usr/bin/env python3

import sys
import time
import usb.core
import usb.util

INPUT_FILE = "flash.bin"

bmRequestType = 0x40
bRequest = 0x03
wIndex = 0x0000

chunk_size = 64

if len(sys.argv) != 2:
    print(f"Kullanım: {sys.argv[0]} <adres>")
    print(f"Örnek:   {sys.argv[0]} 0xEA00")
    sys.exit(1)

try:
    base_address = int(sys.argv[1], 0)
except ValueError:
    print("Geçersiz adres.")
    sys.exit(1)

dev = usb.core.find(idVendor=0x045E, idProduct=0x0770)

if dev is None:
    print("device not found")
    sys.exit(1)

print("found device")

if dev.is_kernel_driver_active(0):
    dev.detach_kernel_driver(0)

with open(INPUT_FILE, "rb") as f:
    data = f.read()

total_size = len(data)
current_address = 0

print(f"File: {INPUT_FILE}")
print(f"Start address: 0x{base_address:04X}")
print(f"Size: {total_size} byte")

while current_address < total_size:

    writebytes = min(chunk_size, total_size - current_address)

    chunk = data[current_address:current_address + writebytes]

    wValue = (base_address + current_address) & 0xFFFF

    dev.ctrl_transfer(
        bmRequestType,
        bRequest,
        wValue,
        wIndex,
        chunk
    )

    current_address += writebytes

    percent = current_address * 100 / total_size

    print(
        f"\rwriting: %{percent:.1f} "
        f"({current_address}/{total_size} byte) "
        f"@ 0x{wValue:04X}",
        end="",
        flush=True
    )

    time.sleep(0.001)

print("\nCompleted")
