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
<br>
Read.py reads memory and saves it to flash.bin.
<br>
Example output from  microsoft vx-700 is given as example_flash.bin
<br>
It is confirmed that read output is not from RAM (or other volatile memory).
