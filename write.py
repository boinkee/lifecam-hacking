#!/usr/bin/env python3
import usb.core
import usb.util
import sys
import time

if len(sys.argv) != 2:
    print(" gimme them!!!")
    print(f"usage:   {sys.argv[0]} input.bin 0x[adress]")
    sys.exit(1)

dev = usb.core.find(idVendor=0x045e, idProduct=0x0770)
if dev is None:
    raise RuntimeError("check device")

if dev.is_kernel_driver_active(0):
    dev.detach_kernel_driver(0)

try:
    cfg = dev.get_active_configuration()
    print("device already configured:", cfg.bConfigurationValue)
except usb.core.USBError as e:
    print("Device not configured", e)
    print("Set configuration")
    dev.set_configuration()


bmRequestType = 0x40 # out command
wIndex = 0x0000
bRequest = 0x03
input = sys.argv[1]
chunk_size = 64
try:
    base = int(sys.argv[2], 0)
except ValueError:
    print("invalid adress!")
    sys.exit(1)

print(f"open file {input}")
with open(input, "rb") as f:
    data = f.read()
total = len(data)
cur_adress = 0

print(f"base adress:0x{base:04X}")
print(f"size:{total} bytes")

while cur_adress < total:
    writebytes = min(chunk_size, total - cur_adress)
    chunk = data[cur_adress:cur_adress + writebytes]
    wValue = (base + cur_adress) & 0xFFFF
    dev.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, chunk)
    cur_adress += writebytes
    percent = cur_adress * 100 / total
    print(f"\rwriting: %{percent:.1f} " f"({cur_adress}/{total} bytes) "f"adress :0x{wValue:04X}", end="", flush=True)
    time.sleep(0.001)
print(f"\nwrote {total}")
