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
On my TPLink Archer C7 this is done by disabling DHCP, and moving the cable from the switch to a LAN port instead of WAN.

Here's a diagram:

![HomeNetwork2018-2](https://raw.githubusercontent.com/SuperThunder/SuperThunder.github.io/master/content/HomeNetwork/NetworkDiagram2018_2.png "A real network, at long last")


If the IP range you are using for pfsense is what your wireless router used to do, you may also need to manually change the LAN IP the router will give itself, otherwise pfsense and the router will fight over who gets to be 192.168.0.1 or the like.


## Why a laptop for pfsense?
Three big reasons: I have it, it wouldn't be in use otherwise, and it fits the specs of an ideal home pfsense box pretty well. It's got an i3-2330M @ 2.2GHz, 6GB RAM, a 750GB hard drive and a battery that can last about 3 hours. The thin profile compared to a desktop helps, too.

So far performance has been great. I don't think I've seen the CPU go above 15% usage, or the RAM go above 25%. The generous disk size allows long term storage of logs and data.

Laptops do generally lack dual NICs or the capacity to get one, but the USB gigabit NIC seems to be working fine. Perhaps it couldn't sustain true gigabit speeds, but in Canada I don't think we're going to get gigabit speeds in most homes for a very long time.

I think a virtual pfsense could also make sense, but then I'd either need another USB NIC and pass both through (or a PCIe one, but those are more expensive), or have all the VMs and all wifi traffic going through the one internal gigabit interface of my VM server. High load on some of the VMs, if it created vCPU contention, could slow down the internet for every device. However, I think I will eventually do virtual pfsense, because having everything running off one VM host is very cool, and is the kind of thing you can recommend to friends or small businesses.


## Suricata and nTopng
Suricata lets us gets alerts (and even block IPs) based on rulesets like EmergingThreats, and nTopng makes it easy to look into what's going on in the network.

For Suricata, I enabled the free community rules (EmergingThreats and Snort). Here's what some alerts look like:

![SuricataAlerts](https://raw.githubusercontent.com/SuperThunder/SuperThunder.github.io/master/content/Screenshots/suricata-retransmissions-alerts.png "Suricata certainly gets excited about things")


For nTop, I turned pretty much every monitor it has on but left the parameters at default. Here's some of the monitors:

![nTop-activeflows](https://raw.githubusercontent.com/SuperThunder/SuperThunder.github.io/master/content/Screenshots/ntop-activeflows-1.png "Active flows")

![nTop-applicatonprotocols](https://raw.githubusercontent.com/SuperThunder/SuperThunder.github.io/master/content/Screenshots/ntop-applicaton-protocols.png "Application protocols")

![nTop-flow](https://raw.githubusercontent.com/SuperThunder/SuperThunder.github.io/master/content/Screenshots/ntop-flow-1.png "Flow Talker diagram")

![nTop-operating-systems](https://raw.githubusercontent.com/SuperThunder/SuperThunder.github.io/master/content/Screenshots/ntop-operating-systems.png "Operating System detection")
