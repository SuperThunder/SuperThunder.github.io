---
layout: post
title: "Adding an OpenVPN server to the home network"
date: 2017-09-06
---
##Port forwarding properly and letting PiVPN do the rest
###(with DynDNS on the router)
Using (PiVPN)[http://www.pivpn.io/] it's only a few button pushes and config details to set up a VPN on a RPi or Debian/Ubuntu server.
The main bother is that the port forwarding needs to be right (1194 or some other port on _UDP_ from the outermost router right to the Pi), and that a DynDNS service is needed if the public IP address will be changing. 
In my case since it's a home internet connection the IP can change at any time, so halfway through the install process I signed up for a no-IP address and set up DDNS on the outermost router.


