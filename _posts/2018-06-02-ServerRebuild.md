---
layout: post
title: "Backing up and Rebuilding my server"
date: 2018-06-02
---
## Reason
So when I built my home server for learning, testing, and some light usage as a NAS and VM host, I threw in 5 old laptop drives ranging from 250GB to 500GB. Some of them report questionable reliability in SMART, and most have poor IO performance.

I bought a suitable 2TB drive to be able to amalgamate all of the storage (media, backups, VMs onto one high performance, modern, drive.

## Things to backup
While nothing would be terrible to lose, it would be annoying. So in advance of changing anything, I prepared a list of things I should backup:
1. the KVM VM qcow2 files and their XML (from `virsh dumpxml`), which should be enough to recreate them on a new host from
2. The KVM network configs, so that the VMs will reconnect properly and keep any static IPs, by `virsh net-dumpxml`
3. Samba config file, for reference when rebuilding (/etc/samba/smb.conf)
4. nginx config that provides access to some VMs.

## Steps
1. Bring server down and take out drives, all 2.5 inch so their important content can be moved around with a USB-to-SATA adapter
2. Install 2TB data, 500GB OS, 320GB VM drive (OS is on same disk as before, VMs will go on repurposed disk)
3. Install Ubuntu server, set up SSH.
4. This is where things get different. I want to have deployment automated in general, so I will use a tool (probably Ansible) at each step to automate deployment. The first step is to automate the samba setup.
5. Set up Ansible scripts for the common things I would always want installed (vim, htop, s-tui, tmux, whatever other tools come to mind).
6. Restore the VMs from backup. This is one-off enough that it might be a quick shell script. Includes restoring the network config and nginx config related to VMs.
7. Import all the data from the previous storage


