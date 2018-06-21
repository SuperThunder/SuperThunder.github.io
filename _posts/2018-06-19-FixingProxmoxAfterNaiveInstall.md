---
layout: post
title: "Things I had to fix in Proxmox after misconfiguring networking during the install"
date: 2018-06-19
---

Proxmox asks for some IPs during install, which I totally misconfigured by bravely trying to get the server quickly working on wifi before bringing it downstairs to the server table. 

What the installer wants is the static IP you'll give the Proxmox host, and the gateway of the network.


## It was DNS
The biggest issue, that I didn't discover until later, was that it writes that IP into /etc/hosts to be able to resolve itself... a lot breaks when the server can't resolve itself. The main symptom I had here was being able to ssh to the server but not being able to access the web interface.


## Setting networking up
After some trial and error I arrived at this `/etc/network/interfaces` file, which bridges the vms to ethernet while also setting the static ip for that ethernet interface.


    auto lo
    iface lo inet loopback

    iface enp1s0 inet manual

    auto vmbr0
    iface vmbr0 inet static
            address 192.168.10.82
            netmask 255.255.255.0
            gateway 192.168.10.1
            bridge_ports enp1s0
            bridge_stp off
            bridge_fd 0


When this was wrong the server would either not get an IP or get an IP but not get any connectivity.



## Corosync also gets the original static IP written in
Another mistake I made was pressing "create cluster" when I had briefly coerced the interfaces file into giving me web GUI access to Proxmox (this broke on a restart). In /etc/corosync/corosync.conf it had the old wonky IP of the server as the IP of the cluster master! Then, whenever it tried to start VMs / Containers by contacting the cluster it was forever "waiting for quorum".

Changing this to the actual IP of the server resolved things.
- It may have also been DNS, but it seems this quorum issue broke my ability to even add CIFS shares to the storage pool


#### Update: I finally found [a relevant post on the forums](https://forum.proxmox.com/threads/properly-flush-cluster-settings-to-recreate-a-new-one.34772/) when the issue of Error 500 No Quorum came up again after a reboot. Corosync.conf gets replaced with the contents of the file in the sqlite3 config database on restart, so the bad config set at installation will persist! It seems like the database record could simply be fixed, but the instructions above are to wipe the VM and corosync config. This did work for me, although I now have to readd my existing VMs from their qcow2 files.

## Proxmox Is Really Cool
Sorting all that out was completely worth it. Proxmox has so far exceeded my expectations in how close it gets to the spine-tingingly expensive vmware that I have seen in many environments.
- The console view just works out of the box, and was not too slow on VNC
- The bridging setup means VMs get their own IPs on your network, which works really well for homelabs and quickly bringing up a VM to try a new thing: it's just as if it was a seperate physical server
- The storage pools, clustering, etc is well exposed in the menus
- Lots of good summary data to see how VM hosts and guests are doing

