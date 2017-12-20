***
layout: post
title: "Planning a Raspberry Pi based MP3 Player"
date: 2017-12-20
***
## Why?
Walking my dogs, waiting for the bus, and walking home in the icy wastes of Canada can be quite boring when there is only the wind to listen to. I usually find trying to set up my phone for music or audiobooks results in frozen fingers.
 Additionally, even if the cold is not too bad, snow or rain can make touchscreens unusable.

There are indeed many cheap MP3 players available, from $3 iPod shuffle look-alikes that seem to have a 50% chance of being DOA to $100 premium products that can also play movies and read ebooks. A huge number of reasonable devices in the $15-50 range copy the design of essentially every popular MP3 player of the last 15 years. What they lack is customizability (most are stuck with quite limited firmware), flashlights (this is important to me for dog-walking), wifi, and in some cases will suffer similar issues as phones in wet conditions.


So, I can make a MP3 player that satisfies my very specific requirements and have fun along the way.

## How?
Using a SBC of some kind, likely a Raspberry Pi Zero or Raspberry Pi 3, an interface to the analog compoments (either a standalone ADC or an Arduino), and a number of cheap and widespread parts. 
 The main parts of an MP3 player, and a likely candidate to provide their functionality, would be:
* Storage: The SD card in the Pi and/or attached USB flash drives
* Display: 1.5 to 2 inch OLED (128x128 color, very clear) or TFT (320x240, still good). Cheap and easy to hook up to Arduino or RPi
* 'Clickwheel': A rotary encoder with a fairly wide and grippy knob. Analog output. Good for scrolling through songs and adjusting volume.
* Up/down/left/right: A game console style D-Pad or PSP style joystick are good candidates for this
* Menu, select, back, etc buttons: Normal click buttons that are made for Arduino/Pi should work but it may be worth the hassle of using rubber dome buttons used in game consoles, game controllers, calculators, etc if they are nicer to use and potentially more waterproof.
* Case: It is easy to buy replacement Gameboy and Gameboy Advance cases. The Gameboy case is sturdy, gives lots of room to work in, and already has a place for the screen and most buttons. It even has a hatch designed for the AAA batteries that would be used for access to USB ports or reset buttons. Designing something myself would involve getting cutting and fitting a sheet of flat plastic into a case, or using something sort of close to the right size and shape like a little plastic storage box.
* Volume control: Not strictly necesarry, but easy to implement with either up/down buttons or a dedicated potentiometer volume knob.
* Flashlight: It turns out even quite bright LED lights do not use that much battery. While the flashlight LEDs on phones seem to be part of the motherboard and unfortunately not often available as standalone parts, there are so many options this should not be difficult to implement. The main consideration is power consumption and ensuring the LED does not explode.
* Speaker: Not entirely necesarry but could be nice to avoid always needing earbuds. Main consideration here is havig a reasonable output power and hooking up to the Raspberry Pi's sound chip properly.
* Battery: USB power banks are so cheap at this point that it would probably be more expensive to get the proper circuit boards and rechargeable batteries required for a DIY solution. The main danger here would be getting a power bank that doesn't handle charging and discharging well, and ensuring it integrates properly into the Gameboy case once stripped out of its own case (physically protected from short circuits, no danger of overheating, capacity LED and power button still accessible).
* Connectivity: The Raspberry Pi should be fast enough that updating over wifi will be sufficient. Otherwise, the player could simply be shut off and the SD card inserted to a PC to have large amounts of music loaded.
* Software: The Raspberry Pi has all sorts of software already available that could do the job. I found several MP3 player interfaces people had made, and the EmulationStation project makes an interface that is easy to use with only buttons and allows launching into your own apps. The main consideration here is keeping power consumption as low as possible, and having everything be completely reliable. Some configuration would need to be done to have the Pi go into a 'sleep' mode with the screen and wifi turned off, and making sure the most is made of the battery by limiting CPU usage. Ideally, everything should be simple and well configured enough that crashes and freezes are not an issue, but to fix any issues a power cycle should be fast and accordingly the Pi's boot up time short.

This project has a surprising amount of overlap with the popular Gameboy Zero project, which involves using a RPi Zero in a salvaged or replacement Gameboy case to make a modern and fast portable game console with the library of everything the RPi Zero can play and emulate. Many people have documented what they did for this project and how they modified their Gameboy case to fit components, which means I can draw ideas for tricky things like integrating a good speaker or adding extra buttons.

## How long?
I expect this project will take me 4-6 months of testing and development in a breadboard and then another 1-2 to plan and build the final setup in the Gameboy case. Since I can only work on it in my spare time the hard parts will take a while to resolve, but this does give the advantage of being able to order cheap parts from ebay or aliexpress without the 1-2 month shipping time being too infuriating. So far (setting up and testing the joystick, rotary encoder, and screen) I have encountered libraries that made the work extremely easy. The interface used would likely be a custom text based UI in C or Python than an X interface, although it is possible the 128x128 color OLED will be large enough to work well with X desktop applications given enough scale adjustments.

