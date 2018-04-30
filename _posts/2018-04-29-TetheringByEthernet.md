---
layout: post
title: "Easy way to connect to Pis by ethernet on Ubuntu"
date: 2018-04-29
---
## Why?
This is the easiest way to get connected to a (potentially) headless computer like a Raspberry Pi, Orange Pi, server without a monitor, etc. It's easy and quite reliable.


## How
Connect your main computer by ethernet cable to the headless computer.

Click the Ubuntu network icon (probably shown as the bars for Wi-Fi)

-> Edit connections

-> Wired connection 1 (or whatever your ethernet connection is called)

-> IPv4 Settings

-> Method: Choose shared to other computers

**Note: if you want to give your main computer a network connection by ethernet later, you'll want to change the method back to Automatic (DHCP)**

Now open a terminal and type `ip a`.

You should see something like 'eth0' or 'enp0s1' with an IP address like 10.0.40.1/24. Somewhere on that 253 IP range from 10.0.40.2 to 10.0.40.253, your attached Pi has been given an IP. I like to go the direct route on finding the assigned IP, so I use nmap.

** be very careful about what you point nmap at! Corporations, governments, and even schools get quite angry if it looks like you're port scanning **

Run the equivalent of `nmap -n 10.0.40.1/24` for the network your main computer has created for the ethernet-attached headless computer. It should come back relatively quickly with 1 result, for your attached computer. Take down that IP, and now you can SSH or VNC in (as set up in the image for that distribution)!


## Notes
Although I usually use it for connecting to Pis, this general method can be useful for all sorts of things. For example, if you built a new desktop but forgot to buy a wifi card for it (or it won't work without drivers), you could use a laptop as a bridge to the internet.

