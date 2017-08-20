---
layout: post
title: "RPi Home Server Part 3"
date: 2017-08-20
---
## Raspberry Pi SSH and SSHFS Gateway
After setting up the RPi to be SSH accesible from the internet, I realized it's only a small step further to SSH from the RPi to other computers on the network.

Specifically, I can now turn my desktop on in the morning and access it from anywhere to run intensive programs or pull a file from my hard drives. The filesystem is a double SSHFS system: on your mobile computer (or some desktop somehwere) you mount the Pi's FS with SSHFS, and then on the Pi you keep the desktop's FS mounted with SSHFS. I can then open a file manager or `cd`  to navigate to any location on my Raspberry Pi or my desktop.
The file paths will look a bit silly though, such as:

    /home/atlaslaptop/Documents/RPiMount/home/atlasRPi/DesktopMount/home/atlasdesktop/Documents/Projects/
    
Speeds with this double SSHFS were not spectacular. Moving a lot of small files, the overhead caused a transfer rate of 700 BYTES per second. Sending single large files (or archives of small files) can get to a more reasonable 1 MB/s.

