---
layout: post
title: "Syncing Rhythmbox Playlists with Dropbox"
date: 2017-10-06
---

Manually moving playlists between computes is pretty annoying. Luckily, Rhythmbox keeps all the playlist and library in XML files in your home directory.
This means we can move the XML files to a cloud-synced directory and then symlink to it.


### Process
1. Backup any important playlists by using File->Playlist->Save to file
2. Close Rhythmbox
3. Copy playlists.xml and rhythmdb.xml from ~/.local/share/rhythmbox to ~/Dropbox/_some directory_/ (other cloud storage providers are available)
4. Rename ~/.local/share/rhythmbox to rhythmbox-BAK
5. Symlink to the directory. My command looked like this: **ln -s ~/Dropbox/Media/Rhythmbox/ ~/.local/share/rhythmbox/**
6. If everything works then you can eventually delete your BAKuped rhythmbox directory

Do this on every computer you want to have synced playlists.
Note that **the relative path to the music files needs to be the same on each computer!**.
For me this is "/home/username/Music/"
You'll also want to have pretty much the exact same library on each computer as they will be sharing the same rhythmdb.

### Notes
I tried symlinking just the playlist file, but rhythmbox would overwrite the symlink with its own playlist information.

It can be a bit tricky to get all the computers on the same page with regards to where to find the music files and getting all the playlists synced.
