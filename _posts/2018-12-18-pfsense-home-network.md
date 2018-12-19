---
layout: post
title: "Redesigning home network for pfsense"
date: 2018-12-18
---
## Why?
With pfsense I can have full control over DHCP, DNS, and other aspects of the network. My TPLink wireless router has to be restarted for small changes (like a new static IP), and provides almost zero information on usage and throughput.

Additionally, I can use traffic analysis plugins for pfsense, or use port mirroring to send all the WAN traffic to a security appliance. This means I can use nTopng+suricata in pfsense, or one of the appliances like SELKS, AlienVault OSSIM, Sophos UTM Home, or SecurityOnion.


## How
Ideally, my servers and networking equipment are all in the basement, except for the wireless access point. After some delicate use of a screwdriver and hammer I got a second network cable down into the basement. 

So now a connection can go from the ISP modem/router to WAN on the pfsense laptop, pfsense provides DHCP and DNS out to the unmanaged switch, which conencts to the server and the wireless router.

The wireless router has DHCP disabled and forwards clients to pfsense.

Here's a diagram:

![HomeNetwork2018-2](https://raw.githubusercontent.com/SuperThunder/SuperThunder.github.io/master/content/HomeNetwork/NetworkDiagram2018_2.png "A real network, at long last")

## Suricata and nTopng
Suricata lets us gets alerts (and even block IPs) based on rulesets like EmergingThreats, and nTopng makes it easy to look into what's going on in the network.
