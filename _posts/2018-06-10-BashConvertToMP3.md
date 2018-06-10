---
layout: post
title: "Automatically convert folder of videos/flac to MP3"
date: 2018-06-10
---

    #!/bin/bash

    for i in *.{mp4,mkv,webm,flac} ; do 
	    # remove the .extension (so we can append .mp3 later) 
	    name=`echo $i | sed 's/\.[^.]*$//'` 
	    echo $name
	    ffmpeg -i "$i" -acodec libmp3lame ./MP3-Conversions/"$name".mp3
    done


Which puts the converted files into a local "MP3-Conversions" directory. The *.{} structure can take more filetypes like ogg.


## Performance

It does put quite a strain on your CPU. However, my laptop was able to get through a few (~5) hours of various formats in only 30 minutes on battery.

I believe the exact choice of codec can affect the transcoding speed and quality, but libmp3lame is fairly widely recommended.
