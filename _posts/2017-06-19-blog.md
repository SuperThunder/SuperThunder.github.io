---
layout: post
title: "Dual Partition USB boot disk"
date: 2017-06-19
---

# Making a USB boot disk that has a bootable partition and a normal storage partition
### (Writing a quick post here to remind myself how to do this)

I formatted the 16GB (actual: 14.9 GiB) as 4.096GB for BOOT and 10.8 for STORAGE.

Then I used UNetBootIn to write the Xubuntu 16.04 x64 image to the boot partition.
However, UNetBootIn seems to just do a simple copy to the partition.

So after that you also need to set the 'boot' flag on the partition to True.

I've stuck around on boot CDs for a while but I could get used to having a complete and ready workspace on a USB key.
