---
layout: post
title: "Backing up and Rebuilding my server"
date: 2018-06-02
---
## Reason
So when I built my home server for learning, testing, and some light usage as a NAS and VM host, I threw in 5 old laptop drives ranging from 250GB to 500GB. Some of them report questionable reliability in SMART, and most have poor IO performance.

I bought a suitable 2TB drive to be able to amalgamate all of the storage (media, backups, VMs) onto one high performancea and modern drive.

## Things to backup
While nothing would be terrible to lose, it would be annoying. So in advance of changing anything, I prepared a list of things I should backup:
1. the KVM VM qcow2 files and their XML (from `virsh dumpxml`), which should be enough to recreate them on a new host from
2. The KVM network configs, so that the VMs will reconnect properly and keep any static IPs, by `virsh net-dumpxml`
3. Samba config file, for reference when rebuilding (/etc/samba/smb.conf)
4. nginx config that provides access to some VMs.

## Steps
1. Bring server down and take out drives, all 2.5 inch, so their important content can be moved around with a USB-to-SATA adapter
2. Install 2TB data, 500GB OS, 320GB VM drive (OS is on same disk as before, VMs will go on repurposed disk)
3. Install Ubuntu server, set up SSH.
4. This is where things get different. I want to have deployment automated in general, so I will use a tool (probably Ansible) at each step to automate deployment. The first step is to automate the samba setup.
5. Set up Ansible scripts for the common things I would always want installed (vim, htop, s-tui, tmux, whatever other tools come to mind).
6. Restore the VMs from backup. This is one-off enough that it might be a quick shell script. Includes restoring the network config and nginx config related to VMs.
7. Import all the data from the previous storage

## How it really went (part 1)
Bringing down the server and swapping the drives was no problem. Neither was making an Ubuntu MATE 18.04 install USB with Etcher. However, the partioning was very stubborn as it refused to remove any partition that was claimed by LVM in any way.

In the end, I installed it in "erase everything" mode and then reinstalled with the "something else" (choose your own partioning) mode.

Then, I had all the little usual tasks to do after installation:
- Install openssh-server
- Enable ufw (uncomplicated firewall): `ufw enable`
- Allow ssh in ufw: `ufw allow ssh`
- Install vim, htop, python pip, tmux
- Use pip to install s-tui and Ansible
- Install samba
- Configure samba
- Allow samba in ufw
- Install KVM (libvirt, qemu, etc)
- Install nginx, allow it in ufw


And some more one-off and context specific tasks:
- Make a new directory structure on the 2TB drive and copy things over
    - Video, VM storage directories, backups, software, etc
- Restore the VM images to their new location on the dedicated 320GB drive, then restore the network XML and VM XML
- Setup the two data drives to mount in /etc/fstab

As my goal is to have the server rebuildable by Ansible, I looked at many Ansible tutorials to find one that matched what I was doing. Most did not, they used cloud VMs and also for some reason tended to not state when they had just created a new file, and where they had put it. 

I found [https://opensource.com/article/18/3/manage-your-workstation-configuration-ansible-part-2](this one) which was more reasonable and has some good explicit examples.

After some fiddling, I had a ansible-play folder with
- local.yml
- ansible.cfg
- hosts
- tasks/ directory

And a command of `ansible-playbook -i ./hosts local.yml --ask-sudo-pass -vv` that got the whole thing started.

Ansible.cfg is simply

    [defaults]
    inventory = hosts

hosts is a basic setup, mostly to point it back at the local server

    [local]
    127.0.0.1

    [home]
    192.168.x.b
    192.168.x.a

    [pi]
    192.168.x.a

    [server]
    192.168.x.b

local.yml currently installs some software and creates an ansible user

    - hosts: localhost
      become: true
      pre_tasks:
            - name: update repos
              apt: update_cache=yes
              changed_when: False

      tasks:
            - include: tasks/install-core.yml
            - include: tasks/users.yml

tasks/install-core.yml

    - name: Install core programs
      apt: 
            name: "\{\{ item \}\}" 
            state: present
      with_items:
            - htop
            - tmux
            - vim
            - samba
            - cifs-utils
            - qemu-kvm
            - libvirt-bin
            - bridge-utils
            - cpu-checker
            - virtinst
            - nginx

tasks/users.yml

    - name: create ansible user
      user: name=ansible uid=850



In the future the ansible user should be setup so that there is no need for a manual sudo prompt, but this works reasonably for a one-time server setup sort of thing.

At this stage samba still needs to be configured, the ufw rules need to be automated, and the VMs are not imported.

I did the ufw stuff with tasks/ufw-rules.yml:

    - name: Enable ufw, for now default policy of allow
      ufw:
            state: enabled
            policy: allow

    - name: Run the ufw app commands for allowed services
      command: sudo ufw allow '{{ item }}'
      with_items:
              - ssh
              - samba
              - Nginx Full

The use of of 'command' instead of the ufw module for Ansible is a bit hacky, but I couldn't see any ufw module features to allow ufw named services.


