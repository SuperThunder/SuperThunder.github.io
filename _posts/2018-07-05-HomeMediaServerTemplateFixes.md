---
layout: post
title: "Things I had to change and other fixes to the cool HardHero/Homeserver Ansible+Docker Media Server setup"
date: 2018-07-05
---

The full details are in my fork on Github, but there are some main themes to the changes. 
I ran Ansible on my control VM in Proxmox, but any Linux computer on your local network should work.
The media server ran on a 2 vCPU / 4GB RAM VM. This seemed to be enough power for everything.

## Broad instructions
In a few places I think the instructions are vague for those newer to Ansible or Docker, so for clarity and completeness I elaborated on them. They are the things I spent tens of minutes of my life trying to figure out.


## IP addresses and usernames
In a few places there are hardcoded IPs and usernames that will make things outright break in your environment or confuse you as to why something isn't working properly. There are a number of files that need to be changed, so I documented all of them.

One of the bigger IPs is of your NAS, the storage of the VMs is broken without it.

## Docker mounts and limited local storage
By default, the docker folder exports (making a folder in the host OS used by the container, often for data or config persistance and sharing) and the VMs are fairly limited. 

For Plex this meant I couldn't point it at my existing media folders, which makes it hard to use as a media center ;)

For Transmission, this meant the incomplete download folder was limited to the host OS's disk size, which in my VMs is around 20GB total. Transmission was easily maxing this out and causing issues. I couldn't make transmission change its usage /data/incomplete, so the solution is to make docker export that entirely to a destination on the NAS.


## Misc: Transmission Web UI
The default transmission web UI is fairly limited in features, especially compared to what transmission can do that is easily done in the desktop client. For example, you can't download only some files in a torrent.

I found there's [a Chinese-made version](https://github.com/ronggang/transmission-web-control/wiki) that is easy to install. It seemed like it was maybe a bit slower, but at the same time the media server VM was under heavy load.


