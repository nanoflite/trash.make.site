---
title: "BitESC - Electronic Speedcontroller for bitcars"
date: "2005-10-28"
categories: 
  - "electronics"
  - "indoor_rc"
coverImage: "bitesc_overview.jpg"
---

[![](images/bitesc_164x132.jpg "bitesc_164x132")](https://vandenbran.de/wp-content/uploads/2008/05/bitesc_164x132.jpg)The BitESC is a small electronic speed controller for those little RC cars like the MicroSizer / BitChar-G. It can be used in a small RC plane to have some control over the speed of the motor. The speed of the motor ramps up or down, depending on which of the buttons on the transmitter you press. If no button is pressed, the ESC will ramp the throttle down to a stop after a few seconds. This safety net comes in handy when the plane flies out of transmitter reach.

## How to use

[![](images/bitesc_overview.jpg "bitesc_overview")](https://vandenbran.de/wp-content/uploads/2008/05/bitesc_overview.jpg)The BitESC weighs in at 0.3 grams, without leads, and has a size of 9 mm x 12 mm. It uses an IRLM 2502 to drive the motor and can pull 1.5 A continuous. The microprocessor used is an Atmel AVR 2343 which runs at 1Mhz.

To be able to use the BitESC, you'll first need to read about the different modifications required on either the transmitter and the reciever. You can read more about how to modify the receiver of a BitChar-G car at the following topics on rcgroups.com:

- [Bitcharger conversion](http://www.rcgroups.com/forums/showthread.php?t=74227)
- [Bitcharger receiver mods](http://www.rcgroups.com/forums/showthread.php?t=94563)
- [Bitcharger TX mods](http://www.rcgroups.com/forums/showthread.php?t=94107)

To get the best results, it is adviced to modify the receiver by adding a longer antenna. I use 1/8 of the wavelength, for 57MHz that gives an antenna length of approx. 63 cm. After extending the antenna, you should retune the receiver by adjusting the coil.

The best hack for the transmitter is to increase the power to the RF circuit and removing the cripple cap, if your TX has one.

This BitESC should cope easily with motor noise. I use a KP00 without a noise reduction capacitor on the Cootie and it works just fine. Although it is a very good idea to add a noise reduction cap to the motor.

The BitESC expects 5 leads to be soldered. The next schematic shows the wiring diagram. The negative of the motor is connected to the BitESC, the other lead goes to the plus lead of the battery (BAT+). The BitESC contains a small RC filter to filter out motor noise.

[![](images/bitesc.gif "bitesc")](https://vandenbran.de/wp-content/uploads/2008/05/bitesc.gif)

## Example

Here's a photo of my Cootie (Designed by [Ralph Bradley](http://www.parmodels.com/)), which I equipped with a BitChar-G receiver and my BitESC. The actuator is connected to the H-bridge on the receiver, which normally connects to the motor and provides forward and backwards motion. The BitESC is connected to the left and right channels. To be able to use the transmitter comfortably, you'll need to switch the controls.

[![](images/bitcootie.jpg "bitcootie")](https://vandenbran.de/wp-content/uploads/2008/05/bitcootie.jpg)

## Schematic

[![](images/bitesc_schema.gif "bitesc_schema")](https://vandenbran.de/wp-content/uploads/2008/05/bitesc_schema.gif)

## Making a BitESC yourself

If you want to make the BitESC yourself, the next information should get you going. Here's the link to the PCB layout, assembly code and hex file.

- [PCB layout](https://vandenbran.de/wp-content/uploads/2008/05/bitesc.pdf)
- [Source code](https://vandenbran.de/wp-content/uploads/2008/05/bitesc.asm)
- [HEX file](https://vandenbran.de/wp-content/uploads/2008/05/bitesc.hex)

I can provide a programmed 2343 and/or a PCB and/or the components, for those who want to solder the BitESC, but so not want to make the PCB or program the MCU.

Here's a printout of the assembly source.

; BitESC
; (c) 2004 Johan Van den Brande

.include "2343def.inc"

.equ TIMEBASE\_TICK = 15000
.equ SAFETY = 25
.equ PWM\_MAX = 63
.equ ESC\_POS\_MAX = 15

.equ esc\_bit = 0
.equ down\_bit = 3
.equ up\_bit = 4

.equ PORTB\_INIT = (1<<down\_bit) | (1<<up\_bit)
.equ DDRB\_INIT = 1<<esc\_bit

.def tmp       = R16
.def esc\_value   = R17
.def esc\_pos    = R18
.def pwm\_value   = R19
.def safety      = R20

.def timebase\_l   = R24
.def timebase\_h = R25

.macro loadesc
ldi   ZL,LOW(2\*esc\_values)
ldi   ZH,HIGH(2\*esc\_values)
clr   tmp
add   ZL,esc\_pos
add ZH,tmp
lpm
mov   esc\_value, R0
.endmacro

.cseg
.org $0000
rjmp   main

main:
ldi      tmp,LOW(RAMEND)
out      SPL,tmp

ldi      esc\_pos, 0
ldi      safety, SAFETY
ldi      timebase\_l, LOW(TIMEBASE\_TICK)
ldi      timebase\_h,   HIGH(TIMEBASE\_TICK)
ldi      tmp, PORTB\_INIT
out      PORTB, tmp
ldi      tmp, DDRB\_INIT
out      DDRB, tmp

loadesc

loop:
; pwm
ldi      tmp, PORTB\_INIT | (1<<esc\_bit)
cp      pwm\_value, esc\_value
brlt   skip
cbr      tmp, 1<<esc\_bit
skip:
out      PORTB, tmp
inc      pwm\_value
andi   pwm\_value, PWM\_MAX

; check timebase
sbiw   timebase\_l, 1
brne   loop

ldi      timebase\_l, LOW(TIMEBASE\_TICK)
ldi      timebase\_h,   HIGH(TIMEBASE\_TICK)

; read input states
sbic   PINB, down\_bit
rjmp   skip\_down
; reset safety
ldi      safety, SAFETY
; motor --
cpi      esc\_pos, 0
breq   skip\_down
dec      esc\_pos
skip\_down:

sbic   PINB, up\_bit
rjmp   skip\_up
; reset safety
ldi      safety, SAFETY
; motor ++
cpi      esc\_pos, ESC\_POS\_MAX
brge   skip\_up
inc      esc\_pos
skip\_up:

cpi    safety, 0
breq   safety\_powerdown
dec    safety
rjmp   safety\_proceed
safety\_powerdown:
cpi      esc\_pos, 0
breq   safety\_proceed
dec      esc\_pos
safety\_proceed:

loadesc

rjmp   loop

esc\_values:
.db   0,   2
.db   4,   6
.db   8,   10
.db   13,   16
.db   19,   23
.db   27,   32
.db   38,   46
.db   57,   63
