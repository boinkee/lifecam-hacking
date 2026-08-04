# LifeCam Hacking
General hacking of Microsoft LifeCam VX-700
<br>
It includes
* Reading memory using usb (wowowow)
* Writing memory using usb (not yet)
* Other things.. (added soon)

# Specs 
* Sonix SN9C255BFG MCU (8051 based)
* MXIC 25l512 64KB SPI flash
* Ram :??
* Green Led
# read.py
Read.py reads memory and saves it to flash.bin.
<br>
Example output from  microsoft vx-700 is given as example_flash.bin
<br>
It is confirmed that read output is not from RAM (or other volatile memory).
<br>
Other values are
* 0x00 (write ?)
* 0x03 (write 0x40)
* 0x04 (read 0x0c)
* 0x05
* 0x08

# patch.py 
Patcher for flash.bin
1. code.bin (you wrote)
2. flash.bin (extracted)
3. Combines code.bin with flash.bin at offset 0xEA00 (free space)
4. output: patched.bin
<br>
This is example for how to add code

# tester.py
This is for testing.
<br>
You change bRequest, value, index, etc.
<br>
This is the copy of read.py

# write.py
write.py writes input.bin to the device
But it isnt persistent..

# analyze8051.py
vibe coded. (I dont have time)
<br>
analyzes the flash file and extracts the instruments in .bin.asm format.
