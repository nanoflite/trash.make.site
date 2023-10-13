Some thoughts about my robot lab...

![](images/robotlab_275_71.png "robotlab_275_71")

# Introduction

As long as I can remember, I've been thinkering with stuff; it started with taking apart toys and later on trying to put them back together as well. One thing, robots have always fascinated me ... I always wanted to build one, but never found the time or the right ideas to build one. Some years ago, I started building my first small robot and now it has grown out to a bit more as a simple hobby. I got the idea of creating a small robot that would be easy to build, use and develop software for, hence, the robot lab was founded ...

I started to use this site as a way to show some of the hardware projects I've been involved in. Take a look, and maybe you encounter something you find usefull or amusing ...

# The original idea ...

The purpose of the robot lab was to develop a cheap tabletop autonomous vehicle for my own desktop A.I. research. My goal was (is) to study autonomous vehicles without the need to invest in an expensive robot platform.

# Specifications

These are the (preliminary) design goals of the small robot.

  * COTS components ( common of the shelves ).
  * Powered by an 8-bit RISC processor
  * 8Kb RAM, 512 bytes RAM, 512 bytes EEPROM
  * Stepper or DC motors
  * Modular sensory system: light, touch, Ir
  * Short range (Ir) and long range (Radio) communications
  * Program in BASIC, C (gcc) or Assembly

# Prototypes

I have made some prototypes, most of them run on a subsumption architecture, pioneered by R. Brooks. The walker uses nitinol as actuators and runs from a simple CPG (Central Pattern Generator) programmed into an AT902313.

## The robots

### [Killerbee](../2004-03-20-killer-bee/)

Killerbee is my first attempt at building a nano sumo bot. These bots have a maximum dimension of 25x25x25 mm and a maximum mass of 25 grams. Killerbee uses a custom build gearbox based on 2 small hobby servos. Its brains are a ATMega8 clocked at 16MHz. Power comes from a 90mAh LiPo battery. It has two line sensors at the bottom and one object sensor, on the front. A custom connector at the back provides an ISP programming interface a serial communication port and two terminals to charge the battery. A small SMD switch allows the bot to be switched on/off.

Killerbee is my first attempt at building a nano sumo bot. These bots have a maximum dimension of 25x25x25 mm and a maximum mass of 25 grams.

Killerbee uses a custom build gearbox based on 2 small hobby servos. Its brains are a ATMega8 clocked at 16MHz. Power comes from a 90mAh LiPo battery. It has two line sensors at the bottom and one object sensor, on the front. A custom connector at the back provides an ISP programming interface a serial communication port and two terminals to charge the battery. A small SMD switch allows the bot to be switched on/off.

### [Tavvy](../2002-04-01-tavvy/)

The first robot I build, with the next characteristics:

  * slow
  * power hungry
  * expensive
  * useless sensors
  * a lot of fun to build and program

The actuators of this vehicle are two small hobby servos, patched for continous rotation. It uses a tracked driving mechanism, like a tank, in which a third drive wheel and a driving belt makes the wheels turn. It uses two Ir proximity detectors (SFH900, Siemens), two Ir ambient light detectors(Ir Photo LED) and two pairs of whiskers as the main sensory equipment (Guitar string). Power is drawn from two NiMH 3.6V CMOS batteries and guarantees at least 10 minutes of continuous operation. It has a piezo speaker for making squeeking noices and even has a plug for charging the batteries ... Oh, before I forget, it's brains are a Atmel AVR 2313 running at 4Mhz and the motors are driven by a L293D H-bridge.

### [Stavvy](../2002-04-01-stavvy/)

This robot is build using small stepper motors that are actually used within the dashboard of VolksWagen cars. I bought them at [http://www.didel.com](http://www.didel.com/), where you can find a lot of other interesting robot stuff. They don't generate a lot of torque, but seem to be sufficient to drive a small autonomius vehicle. An other plus is the low power consumption, a simple 9V battery can drive the system for more then a full day.

### [Ladybug](../2003-08-30-ladybug/)

The ladybug uses two motors from a salvaged hobby servos from which the gears were broken. It does not use any gearbox at all, but relies on the small wheels to have a decent speed. I have to say that this approach works and is also used in some commercial (toy) robot kits ([velleman running bug](http://www.velleman.be/Product.asp?lan=1&id=346299)). The only drawback I had was the relative high power consumption of the servo motors. The choice of the batteries was limited due to the small size of the body. I had to settle with some non-chargeable button batteries to power the electronics and some AAAA batteries (rather small) for the two motors.

The brains are (again) a AT90S2313 from Atmel, running at 10Mhz, the motor driver is a L293D, a dual H-bridge with build-in clamp diodes.

### [MicroRover](../2003-07-31-micro-rover/)

To date, this is my most successfull design. It is powered by an Atmel 8535, which means you can write fairly complex applications (8Kb flash). It has 4 tactical sensors, two eyes based on LDR resistors placed in a tube to have directional sensory, one RC5 Ir diode to be able to command the robot using a standard remote control unit and expansion bus on the top of the vehicle (Wireless module has been build).

### [NanoRover](../2003-07-19-nanorover/)

This is one of the most unconventional designs i've build up to date. It does not run straight, but crawls. The reason for this is that both motors are unidirectional. It uses two wristwatch lavet-type motors as it main actuators and uses two whiskers and two directional LDR light sensors for sensing it's environment. The biggest problem with robot is the fragile connection of the wheels to the shaft of the engine.

### [Nitinol based walker](../2005-10-22-nitinol-walker/)

This walking robot is powered by SMA (Shape Memory Alloy) actuators. SMA is also called nitinol, flexinol or muscle wire. Although I knew muscle wire existed for some time, I did not experiment with it because of its high power requirements that are almost not reachable in sub 10 cm robots. After reading about the usage of muscle wire in an artificial lobster ([Neurotechnology for Biomimetic Robots](http://www.neurotechnology.neu.edu/neurotechnology.html)) I got interested again in the subject. You can read more of my endeavors with this walker here (TODO).
