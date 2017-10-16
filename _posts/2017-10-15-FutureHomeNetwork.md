---
layout: post
title: "Reworking my home network servers"
date: 2017-10-15
---

## The Current Setup
After adding a few servers to my home network organically it has grown a bit wonky.
The main issues are
- No DNS server, so no hostnames. As I get to 3-4 servers this makes it a little anooying to constantly type IPs.
- Two seperate file servers due to one being the attached storage for Transmission. 
- The 600GiB dedicated file server is on the DLink network which is 100Mbit speed. While this shouldn't be an issue for Wifi-connected clients, it could slow down server-to-server transfers or slow down transfers if multiple wifi clients are accessing the file server at once.

This is a diagram of the current setup:

![Home Network](https://raw.githubusercontent.com/SuperThunder/SuperThunder.github.io/master/content/HomeNetwork/NetworkDiagram_2017-10-15.png "Current Home Network (3 servers)")

## Fixing the current setup
- Add a DNS server at the Archer C7 (or even ISP modem/router) level. By controlling DNS we can also enforce certain levels of ad/malware blocking.
- The easy way to fix the dual file servers is to merge the Transmission and file server roles into one machine. If we want to get fancy with containment we could make the Transmission server a VM on the file server.
- Since the file server is on a laptop or desktop it's harder to move that to the living room. It can stay connected to the DLink, or we can try to run another ethernet cable from the Archer C7 to the basement.

Since I now understand VMs and libvirt/KVM well enough to use them to deploy useful services, I may add a VM host on the DLink network. It could be the same PC as the file server / transmission server, or a seperate one to not kill the file server because of excessive VM load.

## The Future Setup
This is a rough diagram of what the future setup will look like.

![Future Home Network](https://raw.githubusercontent.com/SuperThunder/SuperThunder.github.io/master/content/HomeNetwork/NetworkDiagramFuture_2017-10-15.png "Home Network after planned changes (2 or 3 servers)")
