---
title: "Setting up a modern toolchain for Vectrex development with CMOC."
date: "2016-02-01"
coverImage: "zombievectrex.jpg"
color: "#000000"
---

Here I'll show you how to set up a toolchain to develop applications in C for the Vectrex game console. You'll end up with a system that allows you to develop programs for the Vectrex in C, run them on an emulator and, if you have the right hardware, run your program straight from your terminal session on a real Vectrex.

A while ago I acquired a Vectrex game console. It is a unique games console because the display is vector graphics based, instead of raster or pixel based as modern computer displays are.

The Vectrex has a 6809 CPU on board, which was not used as often as the MOS 6502 at the time, so I could not fall back to my knowledge about assembler programming for the commodore line of 8 bit computers. Also, it was not really obvious for me if there was a simple way to set up and use a C toolchain like CC65 for the MOS 6502 CPU.

There is a patch for GCC that allows you to compile for the 6809 CPU, but then you are on your own for developing the standard library or BIOS integration. I also tried to grasp the complexity of the Small Device C compiler, which seems to have some support for close cousins of the 6809. But trying to add support for the 6809 would take up too much time.

Then a few months ago I discovered [CMOC](http://perso.b2b2c.ca/sarrazip/dev/cmoc.html), which is a recently developed C compiler for the 6809 that basically targets the Tandy CoCo computer. It installed flawlessly on my macbook and the code looked clean and easy to understand. That got me thinking about adding support for the Vectrex console as a target. So I started to work on it and now I can proudly say that CMOC has support for the Vectrex console since version 0.1.18.

### Installing CMOC on a macbook

CMOC uses autotools as a build system, so we have to install this dependency first. I assume you have [homebrew](http://brew.sh/) set up on your OSX.

    :::SHELL
    $> brew install automake

Install the latest version of CMOC from [http://perso.b2b2c.ca/sarrazip/dev/cmoc.html](http://perso.b2b2c.ca/sarrazip/dev/cmoc.html), which was 0.1.19 when I wrote this.

    :::SHELL
    $> wget http://perso.b2b2c.ca/sarrazip/dev/cmoc-0.1.19.tar.gz
    $> tar zxvf cmoc-0.1.19.tar.gz
    $> cd cmoc-0.1.19
    $> ./autogen.sh
    $> ./configure --prefix=~/Projects/retro/vectrex/tools
    $> make
    $> make install

### Installing LWTOOLS

CMOC depends on [LWTOOLS](http://lwtools.projects.l-w.ca/) for the assembler and linker utilities. CMOC generates an assembly file from the C sources and calls `lwasm` to compile this file.

    :::SHELL
    $> wget http://lwtools.projects.l-w.ca/releases/lwtools/lwtools-4.12.tar.gz
    $> tar zxvf lwtools-4.12.tar.gz
    $> cd lwtools-4-12
    $> make DESTDIR=~/Projects/retro/vectrex/tools
    $> make install

### Setting up a Vectrex emulator.

There are a few options when it comes to choosing a Vectrex emulator for OSX. A good choice is ParaJVE, but the problem with it is that you can't use it from the command line. VecX is another option, the [code is on Github](https://github.com/jhawthorn/vecx) and is cleanly written. I [forked it so I could tweak it a bit to my likings](https://github.com/nanoflite/vecx). For one, I added the option to choose the BIOS ROM with an environment variable. That allows me to use a fast-boot ROM which starts up the Vectrex a bit faster.

You can grab the code of my fork on Github and proceed with the README. Here's a synopsis on how to install VecX, assuming you have Homebrew installed.

    :::SHELL
    $> brew install sdl
    $> brew install sdl_gfx
    $> brew install sdl_image
    $> brew install sdl_mixer
    $> brew install sdl_ttf
    $> cd ~/Projects/retro/vectrex/tools
    $> git clone https://github.com/nanoflite/vecx.git
    $> cd vecx
    $> make

### Setting up support for the VecMulti cartridge

The VecMulti cartridge can be used to play games from a uSD card, but it also has a handy development feature when you use it without SD card. In development mode, you can send a game to the Vectrex by using a serial to USB cable. It is the ideal cartridge for Vectrex development, but the only problem is that it is hard to find. The VecMulti is produced by Richard Hutchinson and although his site is offline (http://www.vectrex.biz/), you can get lucky contacting him.

Because the original tooling is written in [Lazarus](http://www.lazarus-ide.org/), an OSS Delphi Pascal IDE, I was not really keen on using it. I love command line tools, so I set forth developing a Python tool for it. You can find [my VecMulti tool](https://github.com/nanoflite/vecmulti) on Github. Here's how you install it.

    :::SHELL
    $> pip install pyserial
    $> cd ~/Projects/retro/vectrex/tools
    $> git clone https://github.com/nanoflite/vecmulti.git
    $> cd vecmulti
    $> ls

### Setting up the shell environment

Now that we have al the tools installed, let us create a shell environment that ties everything together.

Here's a small shell snippet that you can source to set up the environment. You'll probably need to edit the path a bit to suit your own setup.

    :::SHELL
    CMOC_BIN=~/Projects/retro/vectrex/tools/bin
    LWTOOLS=~/Projects/retro/vectrex/tools/usr/bin
    VECMULTI=~/Projects/retro/vectrex/tools/vecmulti
    VECX=~/Projects/retro/vectrex/tools/vecx
    VECTREX_ROM=$VECX/fastrom.dat
    
    export PATH=$PATH:$CMOC_BIN:$VECMULTI:$VECX:$LWTOOLS
    export VECTREX_ROM

You can set up the enviroment by souring the above file.

    :::SHELL
    $> . vectrex.env

### Hello world

Now let us move on to an example. Here's the source code for a _hello world_ example on the Vectrex.

    :::C
    #include <vectrex/bios.h>
    
    int main()
    {
      while(1)
      {
        wait_retrace();
        intensity(0x7f);
        print_str_c( 0x10, -0x50, "HELLO WORLD!" );
      }
      return 0;
    }

Save this as `hello_world.c` and use the following command in the terminal to compile it.

    :::SHELL
    $> cmoc --vectrex --verbose hello_world.c
     
    Target platform: vectrex
    Preprocessing: hello_world.c
    Preprocessor command: cpp -xc++ -I'/Users/johan/Projects/retro/vectrex/cmoc-dev-bin/share/cmoc' -DVECTREX=1 -U__GNUC__ hello_world.c
    Compiling...
    Code address: $0 (0)
    Data address: $c880 (51328)
    Assembler: /Users/johan/Projects/retro/vectrex/cmoc-dev-bin/share/cmoc/a09
    Assembly language filename: hello_world.asm
    0 error(s), 0 warning(s).
    Assembling: /Users/johan/Projects/retro/vectrex/cmoc-dev-bin/share/cmoc/a09 --includedir='/Users/johan/Projects/retro/vectrex/cmoc-dev-bin/share/cmoc' --entry=0 --target=VECTREX --verbose hello_world.asm
    Preprocessor command: cat hello_world.asm  | cpp -P -traditional  -I'/Users/johan/Projects/retro/vectrex/cmoc-dev-bin/share/cmoc' -DVECTREX=1
    Assembler command: lwasm --pragma=forwardrefmax --list=hello_world.lst --symbols --format=ihex --output=hello_world.hex hello_world.i
    Generating .bin: 'intelhex2cocobin' --no-blocks < 'hello_world.hex' > 'hello_world.bin'

If everything went fine, you should end up with a `hello_world.bin` file, which is runnable on an emulator and on a real Vectrex. To run this on the VecX emulator, you can use the following command:

    :::SHELL
    $> vecx hello_world.bin

If you have the VecMulti cartridge, you are able to run it on a real Vectrex by using a command similar to the one shown here.

    :::SHELL
    $> vecmulti load --port /dev/cu.SLAB_USBtoUART --progress hello_world.bin

### Summary

In this post I told you how to set up a development toolchain for the Vectrex so you can compile and run Vectrex applications written in C using the CMOC C compiler. In a follow up post I'll show you how to automate things a bit further with a Makefile and I'll also talk more about the BIOS routines you can use from CMOC.
