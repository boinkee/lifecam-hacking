#!/usr/bin/python3
# To read the flash over usb, we need specific vendor commands.
# For example bmRequestType C0 and bRequest 0x04.
# And to read a specific area, we need to change the value block.
import sys
import usb.core
import time
# the holy flash file
OUTPUT_FILE = "flash.bin"
dev = usb.core.find(idVendor=0x045E, idProduct=0x0770)

if dev is None:
    raise ValueError("Device not found! Default VID/PID: 045E 0770")
print("found device")

if dev.is_kernel_driver_active(3):
    print("detach kernel driver")
    dev.detach_kernel_driver(3)

try:
    cfg = dev.get_active_configuration()
    print("device already configured", cfg.bConfigurationValue)
except usb.core.USBError as e:
    print("Device not configured", e)
    print("Set configuration")
    dev.set_configuration

bmRequestType = 0xC0
bRequest = 0x04
wIndex = 0x0000
# sizes
total_size = 65536
chunk_size = 255
current_address = 

print(f"Read start File:{OUTPUT_FILE}")

with open(OUTPUT_FILE, "wb") as f:
    while current_address < total_size:
        readbytes = min(chunk_size, total_size - current_address)
        wValue = current_address & 0xFFFF
        # read from flash
        response = dev.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, readbytes)
        # write to file
        f.write(response)
        current_address += readbytes
        percent = (current_address / total_size) * 100
        print(f"\rwriting: %{percent:.1f} ({current_address}/{total_size} byte)", end="", flush=True)
        # make it not overheat
        time.sleep(0.001)

print("\nCompleted")
