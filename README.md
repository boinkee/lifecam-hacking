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
Other values are these:
<br>
bRequest=0x00  OK  len=8  data=0000020000010000
<br>
bRequest=0x03  OK  len=8  data=534e394332353000 > SN9C250 (BFG?)
<br>
bRequest=0x05  OK  len=2  data=0101 
<br>
bRequest=0x08  OK  len=8  data=0000020000010000

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
This doesnt work.
<br>
We need to find the values to write.
<br>
Otherwise it throws an timeout error.

# analyze8051.py
vibe coded. (I dont have time)
<br>
analyzes the flash file and extracts the instruments in .bin.asm format.
