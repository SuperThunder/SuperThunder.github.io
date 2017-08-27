---
layout: post
title: "ISP modem/router to TPLINK router to DLINK router with only double NAT instead of triple NAT"
date: 2017-08-26
---
### What on earth? _Triple NAT_?
The setup here is that my ISP provides a modem/router combination. It has poor wireless performance so it has wifi disabled and one of its LAN ports is plugged into the WAN port of a TPLink Archer C7. This means the ISP router's 192.168.2.100+ IP space is empty except for the Archer C7. The Archer C7's IP space of 192.168.0.100+ has all wireless devices. It also has devices connected to LAN ports; the home servers. As it stands we have the ISP router NATting to 192.168.2.100+ and then one IP in that range (the Archer C7) NATting to 192.168.0.100+, double NAT.

Due to the ISP setup the ISP router has to be near the main cable TV box as it provices the network connection for it. The main TV box is next to the main TV in the house as it wouldn't make sense to put it elsewhere. The ISP's modem/router also handles landline phone so the base unit of the cordless phone set has to be plugged into the phone jack on the modem/router. This means there's a lot of little boxes next to the main TV and not a lot of extra room (two routers, a TV box, a cordless phone station, and a power bar for all these devices).

So, enter all the home servers I want to experiment with. A mix of Raspberry Pis (see previous posts) and repurposed old laptops, it becomes a real mess to have them all connected near the TV area. Luckily, the previous owners of the house drilled a hole in the floor for their competing ISP's cable TV service. After ripping the severed cable out of the insulation foam, I was able to drop an ethernet cable down from the Archer C7 to a set of shelving in the basement. This ethernet cable is the link from our main network to an old DLink running DD-WRT that has a perfectly respectable 4 LAN ports for our purposes.

The issue is, the way things work when you just keep plugging routers into each other is that each new router is another network NAT'ed from the previous in which devices from previous networks are isolated from devices on the next level of network 'down'. None of the servers on the DLink router can be SSH'ed or browsed to by all the regular devices on the TPLink router!

### The Solution
I could have just port forwarded like crazy for everything I needed on the DLink. A port forward for SSH to every server, a port forward for every webserver, a port forward for every media/file/torrent server. However, there is a better way. 
Instead of using the DLink router as another gateway creating another network, I changed it to add to the Archer C7 network (after some false starts and physical config resets)
1. Plug an ethernet cable into the main router (Archer C7) LAN and secondary router (DLink) LAN (not WAN! If we use WAN it becomes more difficult to join the two networks)
2. Get the MAC of the secondary router and reserve a static address for it in the DHCP of the main router. 
- I gave 192.168.0.2 to the DLink on the recommendation of a guide; I am still unsure whether it has significance as the second lowest IP address in the range.
3. Set the secondary router so that it is not giving out IP addresses and tells clients to get their IP addresses from the main router.
- For the DLink on DDWRT, I changed it to router mode instead of gateway mode
- Turn DHCP mode from 'server' to 'forwarder'
- Set the Gateway/DNS to the IP of the main router (for me, 192.168.0.1)
- Set the secondary router's IP in its control panel as 192.168.0.2 (the address I reserved for it in the main router)
4. Reboot both routers if they need it to make the config changes


### Too Long Diagram Read
![Home Network Diagram]()

### Notes
I found out this [is called cascading](https://www.linksys.com/ca/support-article?articleNum=132275) for wired connections and bridging for wireless connections. 
