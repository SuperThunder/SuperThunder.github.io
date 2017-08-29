---
layout: post
title: "VPN-connected torrent server that is still accesible as a website or by SSH with local file sharing"
date: 2017-08-28
---
### Using one Raspberry Pi for absolutely everything
Following the guide in the Notes section I added VPNed torrent capability to the Pi3 that already does the SSH forwarding and speedtests.
The speeds through the VPN were good and the guide configures it to have minimal chance of IP leaks. However, there still needs to be a way to get the files off the RPi once downloaded.

While this solution may result in painful speeds, the easiest way to get the downloaded files is to set up a SAMBA share.

If I want the files to be accessible from the internet in the future I will need something more secure (perhaps an owncloud setup pointed at the folder). The Transmission webpage would also potentially need to be accesibble from the internet.

### Samba setup
I pointed the SAMBA share at the /home/vpn/Download folder used to store the torrent downloads. I set up the SAMBA share as public and guest accessible since only local network connections are able to get to the Pi on anything but port 22 (which is forwarded through two routers).

Trying to get samba running with systemctl resulted in various errors about missing runlevels or masks. `sudo systemctl enable smbd.service nmbd.service` seems to have worked as the share is accessible, and the smbd process is running.

After getting this all setup I changed the samba and transmission config files to point at a portable hard drive instead of a location on the very small SD card.

### Aside
The issues I was having with Transmission's website not showing up for LAN-connected computers seems to have resolved itself by redoing everything from scratch on a RPi3 _except_ install MoinMoin. My best guess is that nginx was assuming every incoming connection was for it but then discarding them when it didn't find a website bound to that port.

### Notes
This guide [on VPN split tunneling](https://www.htpcguides.com/force-torrent-traffic-vpn-split-tunnel-debian-8-ubuntu-16-04/ "VPN Split Tunnel") was easy to follow and worked very well. It even has specific directions for whether you're using Ubuntu, Debian, or Raspbian. (Part 2)[https://www.htpcguides.com/configure-transmission-for-vpn-split-tunneling-ubuntu-16-04-debian-8/] sets up the reverse proxy so that Transmission's web interface can be accesed even while all Transmission traffic is going through the VPN.

(A really old school guide to BitTorrent)[http://lifehacker.com/285489/a-beginners-guide-to-bittorrent]

(SAMBA guide from magpi)[https://www.raspberrypi.org/magpi/samba-file-server/]
