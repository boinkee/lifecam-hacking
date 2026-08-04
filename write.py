#!/usr/bin/env python3
import usb.core
import usb.util

dev = usb.core.find(idVendor=045e, idProduct=0770)
if dev is None:
    raise RuntimeError("check device")

try:
    cfg = dev.get_active_configuration()
    print("device already configured", cfg.bConfigurationValue)
except usb.core.USBError as e:
    print("Device not configured", e)
    print("Set configuration")
    dev.set_configuration()

bmRequestType = 0x40
wIndex = 0x0000
wValue = 0x0000

print("start")
for req in range(0x100):
    try:
        dev.ctrl_transfer(bmRequestType, req, wIndex, wValue, None, timeout=100)
        print(f"bRequest=0x{req:02X}  seems good")
    except usb.core.USBError:
        pass
print ("done")
