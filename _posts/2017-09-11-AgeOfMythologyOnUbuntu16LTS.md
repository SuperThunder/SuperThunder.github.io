---
layout: post
title: "Age of Mythology Gold on Ubuntu 16.04 LTS using PlayOnLinux and ISO files"
date: 2017-09-06
---
### Required files and packages
I used ISOs made from the box set of Age of Mythology Gold purchased sometime in 2007 and copied to ISO sometime in 2010.
The ISOs:
 - AOM_D1.iso
 - AOM_D2.iso
 - AOMX.iso
 
I also have both the Age of Mythology and Titan's Expansion original CD keys in a text file with the ISOs. Avoiding the CD key check would require questionable copy protection crackers.

A recent version of PlayOnLinux. In the config for Wine version I changed from the system default to 1.7.55

gcdemu, a virtual CD drive creater for Ubuntu. This is how the ISOs are mounted in a way the installer will accept. I followed (this guide)[http://ubuntuhandbook.org/index.php/2014/12/install-virtual-cd-drive-cdemu-ubuntu-1404/].

### Installation
The PlayOnLinux "Age of Mythology Gold Edition (Ubisoft)" template did not work for me as it wouldn't detect the installation CD no matter what I did.

So instead I used the "install a non-listed program" option and used gcdemu mounting to mount the ISOs. Getting CD #2 into the same drive that CD #1 had occupied took a bit of fiddling with the "drives" options under "configure wine" and gcdemu but it got there eventually. 
What I ended up doing is creating a second virtual drive in gcdemu to mount AOM\_D2.iso. I then switched the D: CD drive in Wine to point at the new virtual mount instead of the original AOM\_D1.iso mount.

PlayOnLinux will complain about a crash in the background but this is normal. Once the AoM installer is finished the PlayOnLinux installer can be completed, including the creation of a desktop shorcut to Age of Mythology.

### Configuration
The most immediate issue I had was the complete lack of good graphics options. In 2002 Intel integrated graphics was not very good, so the game sees Intel integrated and reverts to only offering very safe graphics options (1024x768 16bit).
In most cases I believe AoM will be using the gfxconfig/i845.gfx file to provide the graphics options for modern Intel integrated chips. What I did was back this file up, copy the geforce3.gfx file into a new i845.gfx file, and then go into the file and manually define the resolution options I wanted (mainly 1600x900x32).
(This post)[http://fremycompany.com/BG/2013/Age-of-Mythology-no-fog-of-war-transparency-custom-resolutions-274/] outlined the process I followed.

I also wanted AoM to be windowed, so I set Wine to create a virtual 1600x900 desktop. In Age of Mythology I ticked the "Play in window" option in the graphics settings as well as selecting my 1600x900x32 graphics option.

By pure coincidence I found a way to get widescreen fullscreen with minimal apparent stretching. At the main menu in a widescreen window, press Alt-Enter to fullscreen the game. It takes on a 4:3 aspect ratio in fullscreen. Hit Alt-Enter again to go back to windowed, where it will be a 4:3 window. Go into the graphics setting, open the resolution list, and select the already selected "1600x900x32" resolution option then click OK. Somehow this makes the game fullscreen in widescreen with no stretching and very smooth Alt-Tabbing

### Things that have caused issues so far
- If I have VirtualBox open, Age of Mythology can't brought into focus after an Alt-Enter. This did not surprise me as VirtualBox tends to interfere with other windows all the time (like preventing me from typing into anything but VirtualBox screens until I close every VM and the VM control panel).
- Very occasional crashes with various error messages. The game had usually been running for hours through multiple sleep/wake cycles so this has only been a minor inconvenience.

### Titan's Expansion
- Installing the Titan's Expansion is a very similar process to the base game installation. Instead of making a new virtual drive, run the installation as an 'Overwrite' on the virtual drive you defined for the base game.


