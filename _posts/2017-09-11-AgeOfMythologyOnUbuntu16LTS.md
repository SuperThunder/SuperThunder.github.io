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

qcdemu, a virtual CD drive creater for Ubuntu. This is how the ISOs are mounted in a way the installer will accept. I followed (this guide)[http://ubuntuhandbook.org/index.php/2014/12/install-virtual-cd-drive-cdemu-ubuntu-1404/].

### Installation
The PlayOnLinux "Age of Mythology Gold Edition (Ubisoft)" template did not work for me as it wouldn't detect the installation CD no matter what I did.

So instead I used the "install a non-listed program" option and used qcdemu mounting to mount the ISOs. Getting CD #2 into the same drive that CD #1 had occupied took a bit of fiddling with the "drives" options under "configure wine" and qcdemu but it got there eventually.

PlayOnLinux will complain about a crash in the background but this is normal. Once the AoM installer is finished the PlayOnLinux installer can be completed, including the creation of a desktop shorcut to Age of Mythology.

### Configuration
The most immediate issue I had was the complete lack of good graphics options. In 2002 Intel integrated graphics was not very good, so the game sees Intel integrated and reverts to only offering very safe graphics options (1024x768 16bit).
In most cases I believe AoM will be using the gfxconfig/i845.cfg file to provide the graphics options for modern Intel integrated chips. What I did was back this file up, copy the geforce3.cfg file into a new i845.cfg file, and then go into the file and manually define the resolution options I wanted (mainly 1600x900x32).
(This post)[http://fremycompany.com/BG/2013/Age-of-Mythology-no-fog-of-war-transparency-custom-resolutions-274/] outlined the process I followed.

I also wanted AoM to be windowed, so I set Wine to create a virtual 1600x900 desktop. In PlayOnLinux -> Configure -> Age of Mythology -> Wine -> Configure Wine -> Graphics I ticked the "Emulate a virtual desktop" option and set its size to 1600x900. I learned this from (this stackoverflow thread)[https://askubuntu.com/questions/290764/how-to-start-a-playonlinux-game-windowed]




