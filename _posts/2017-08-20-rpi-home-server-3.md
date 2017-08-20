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
(atlas is the example user in this case)

Speeds with this double SSHFS were not spectacular. Moving a lot of small files, the overhead caused a transfer rate of 700 BYTES per second. Sending single large files (or archives of small files) can get to a more reasonable 1 MB/s.


## How to set it up from start to finish
None of the steps involved are too complicated, but have little wiggle room (if you don't port forward it won't work, if you get the wrong IP it won't work, etc)
Making the environment:
1. Set up the SSH server on your desktop/home computer. I set this up with regular password login.
2. Set up the SSH server on the Rapsberry Pi. Since this is externally facing I configured it to be RSA private/public key login only, with port 22 on the Pi forwarded to a port between 20,000 and 60,000 on the router. It's also good practice to remove the default 'pi' user and set a strong account password for login in from other users or sudo.
3. Set up SSH on your connecting device (probably a laptop). Make sure you note the IP of your home router or set up a dynamic DNS service.

## How to login and mount the filesystems
1. Ensure the desktop at home is turned on, connected, and sshd is running (it should automatically come up)
2. Ensure the raspberry pi is running, connected, and sshd is running.
3. Login to the Pi with SSH from your external device. Mount the desktop's filesystem: `sshfs desktopuser@<desktopip>:/ ./<mountpoint on your Pi> -p 22`
4. Mount the Pi's filesystem on your external device: `sshfs piuser@<ExternalRouterIP> ./<mountpoint on your device> -p <PortNumber>`
