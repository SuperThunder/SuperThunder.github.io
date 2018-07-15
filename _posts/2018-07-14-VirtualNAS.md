---
layout: post
title: "OpenMediaVault Virtual NAS on Proxmox"
date: 2018-07-05
---

## Why?
After setting up my Proxmox VM server I had two HP Z400s idling essentially all the time, and plenty of free CPU/RAM capacity left on the VM host.

If the NAS functions could be virtualized, which after testing I found they could, then I could free up a machine and reduce my power consumption.

In a home setting I think a virtual NAS can make a lot of sense. A single server box virtualizing everything means you can consolidate and efficiently allocate RAM and CPU, as well as taking up less space and power. This setup is probably not safe or redundant enough to be suited for small business or enterprise environments, although there are interesting 'hyperconverged' options now available in those spaces.

## What
I used OpenMediaVault in a Proxmox VM with 1 core and 2GB of RAM, which so far has caused no issues, and 1GB or even 512MB would probably work fine. The install disk size does not need to be big, I allocated 10GB and it only uses 20% of it.

The method I used to have the disks in the OMV VM was to use the passthrough features of QEMU, so that the disks are totally managed by OMV itself.

## How

### Before the first boot
- Make the Proxmox VM with the suitable resources allocated and the OMV install ISO loaded
- SSH into (or use the console of) your Proxmox host. Do any partitioning/formatting of the disks needed. Run `lsblk -f` to get the UUIDs of the disks you want to use.
- Adjust and the run the following command to passthrough the disks you want used

    qm set 108 -scsi1 /dev/disk/by-uuid/your-uuid-chars
    
- '108' here is the ID of the VM, so set this to whatever ID your OMV VM has. scsi1 means this is the second disk attached to the virtual SCSI interface, the first being the boot disk you made. You also have 'ide' and 'sata' as options, but SCSI is the best performing on Proxmox. 
- If you are attaching multiple disks, be sure to increment the number after 'scsi' each time.

### Install
- Start the OMV VM.
- Go through the install, choose the right disk (the small 10GB one) as the OS disk.
- The install is fairly straightforward, make sure to use strong passwords. These passwords are protecting your data!
- Once done, let the VM reboot. Login by console (we will enable SSH later) and take note of the VM's MAC address, and go configure a static IP. Reboot the VM so it takes that IP.

### Configure admin password
- Connect to the IP of the VM, you should be greeted with the login page. Login with the default `admin / openmediavault` credentials.
- Change the default credentials by going to General Settings -> web password. Again, set a good password and take note of it somewhere safe.

### Configure users
- Create the users you want in Access Rights Management -> Users. I usually stick with a simple 'nas' general user, and then users for specific services.
- Create the groups you want in Access Rights Management -> Groups, and add users to those groups. I like to assign permissions to groups rather than directly to users, so that you can see which user did something even if they have identical access.

### Configure disks
- in Storage -> File Systems, mount the disks that you passed through. I had already partitioned and made filesystems on mine, but you can also do that here. 

### Configure shared folders
- This will not share any of your folders directly, but make them available for sharing by the various services
- Click 'Add', then say what filesystem and what path on that filesystem, and the general permissions setup (ex: Admin has RW, users have R, guests have no access).
- Then, click on the shared folder then click on 'Privileges' above. Set what Groups / Users you want to have access to that share!

### Enable services
- Under Services, enable the ones you want. For me that is SMB and SSH.

### Configure shares
- This is where you will need to explore a bit as your needs are probably different than mine. My needs were for a few SMB shares with various users able to access them.
- In Services -> SMB, go to 'Shares', add all the SMB shares you want by saying what shared folder and the policy for guests.

## Notes
- If you are migrating a physical NAS to a virtual one, you will probably want to simply drop the disks in and configure the exact same shares. Depending on your network setup, you will probably have to adjust the IP used in your clients.
- Do not use a virtual NAS to store VM drives or ISOs without thinking about it. Probably, you will need to remember that after Proxmox the OMV VM needs to come up. There are some risks of circular dependencies here.

