---
layout: post
title: "Nextcloud and DNS overrides"
date: 2019-06-06
---
## Why?
Nextcloud is a very easy way to get something approximating your own Dropbox or Google Drive (and it even has a Linux client unlike Google Drive!)

I set it up on top of my existing "everything crammed into one box" VM host + NAS + server VM architecture. I more or less just made a CIFS share for it and mounted it in the VM, then pointed the Nextcloud install at that path. It's a bit flaky on VM host reboots, but very good for the low price of free and a day or so taken to do the setup.

But enough of Nextcloud, it's well documented elsewhere.

Once I installed Nextcloud, I naturally wanted to access it from the internet, so I set up a suitable port forward on my home IP that is tracked by a Dynamic DNS address.

So, within my local network, the Nextcloud VM's private IP or hostname work well and from the internet my dynamic DNS works well. But, trying to access your external IP from within a NAT'd network doesn't work so well.

The Nextcloud clients expect a single IP or DNS address to point to, and of course we want to get file sync while away from the home LAN.

So I needed to have the DNS lookup point to the local server instead when doing it inside my LAN. Luckily, my router is pfsense 2.4 which has some real features vs an ISP omnicheapbox. Unfortunately, I don't have much control over my DDNS domain, so nice subdomains like `nextcloud.myddns.ddnshost.com` are not possible.


## Final working setup

- Turn off any limiters as these sadly somehow break the firewall rules being used. This is a bug that was supposedly fixed a few years ago in pfsense but I seem to have run into it again.
- Create a Host Override for my DDNS domain in pfsense, and make it resolve to the pfsense server itself.
- Create a NAT port forward rule on the **LAN interface** that redirects traffic to the pfsense server on the special high port I use for Nextcloud, which redirects to https on the Nextcloud server itself. (A similar rule on WAN exists for the Nextcloud traffic coming from the internet).
-- I used destination 'this firewall' for the NAT rule



Apparently the more elegant (from a configuration viewpoint) method is to use 'NAT reflection' which sees that you want to get at your external IP from internally, and processes the packets as if they were coming externally. Limiters can also break this.

Now that I think about it, pfsense gets an IP from the ISP omnicheapbox, it doesn't have the true external IP, so that may have something to do with it
