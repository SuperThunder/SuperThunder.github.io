---
layout: post
title: "Figuring out infrared on the OrangePi Zero (in which I am an enormously silly goose)"
date: 2018-05-12
---
## Intro
On the expansion board for the OrangePi Zero there is IR, a microphone, a TV-Out/3.5mm-out jack, and 2 USB ports.

This post is about what I did with the IR and the common 21 button IR remote that takes CR2025 batteries. Mine say "Car MP3" at the bottom but this seems to be on only some versions.
![This is what it looks like](https://raw.githubusercontent.com/SuperThunder/SuperThunder.github.io/master/content/Electronics/Remote-IR-CarMP3.jpg "Car MP3 Remote")

[This gist](https://gist.github.com/steakknife/e419241095f1272ee60f5174f7759867) seems to be the exact same remote in terms of layout and hex codes.

## Notes
The following section is a lot of me making changes without restarting the relevant service. Skip to the end for the conclusion.

Not written here is the fiddling with the files like /etc/lirc/hardware.conf to set the correct driver values.

## Testing Remote
I was able to get a helpful stream of hex code, sequence count, and corresponding key as well as the config file involved by running `irw`.
irw yields, with some button pushing on the remote:

	0000000000ff22dd 00 KEY_PREVIOUS /root/lircd.conf.conf
	0000000000ffe01f 00 KEY_VOLUMEDOWN /root/lircd.conf.conf
	0000000000ffe01f 01 KEY_VOLUMEDOWN /root/lircd.conf.conf
	0000000000ffa857 00 KEY_VOLUMEUP /root/lircd.conf.conf
	0000000000ffa857 01 KEY_VOLUMEUP /root/lircd.conf.conf
	0000000000ff6897 00 KEY_0 /root/lircd.conf.conf
	0000000000ff6897 01 KEY_0 /root/lircd.conf.conf
	0000000000ffe01f 00 KEY_VOLUMEDOWN /root/lircd.conf.conf
	0000000000ff30cf 00 KEY_1 /root/lircd.conf.conf
	0000000000ff18e7 00 KEY_2 /root/lircd.conf.conf
	0000000000ff02fd 00 KEY_NEXT /root/lircd.conf.conf
	0000000000ff02fd 00 KEY_NEXT /root/lircd.conf.conf
	0000000000ff6897 00 KEY_0 /root/lircd.conf.conf
	0000000000ff38c7 00 KEY_5 /root/lircd.conf.conf
	0000000000ff38c7 01 KEY_5 /root/lircd.conf.conf
	0000000000ff42bd 00 KEY_7 /root/lircd.conf.conf
	0000000000ff52ad 00 KEY_9 /root/lircd.conf.conf
	0000000000ffa25d 00 KEY_CHANNELDOWN /root/lircd.conf.conf
	0000000000ffa25d 01 KEY_CHANNELDOWN /root/lircd.conf.conf
	0000000000ffe21d 00 KEY_CHANNELUP /root/lircd.conf.conf
	0000000000ffe21d 01 KEY_CHANNELUP /root/lircd.conf.conf
	0000000000ff22dd 00 KEY_PREVIOUS /root/lircd.conf.conf
	0000000000ff22dd 01 KEY_PREVIOUS /root/lircd.conf.conf
	0000000000ff02fd 00 KEY_NEXT /root/lircd.conf.conf
	0000000000ffc23d 00 KEY_PLAYPAUSE /root/lircd.conf.conf
	0000000000ffc23d 01 KEY_PLAYPAUSE /root/lircd.conf.conf
	0000000000ffe01f 00 KEY_VOLUMEDOWN /root/lircd.conf.conf
	0000000000ffa857 00 KEY_VOLUMEUP /root/lircd.conf.conf
	0000000000ffa857 01 KEY_VOLUMEUP /root/lircd.conf.conf
	0000000000ff906f 00 KEY_EQUAL /root/lircd.conf.conf
	0000000000ff906f 01 KEY_EQUAL /root/lircd.conf.conf
	0000000000ff6897 00 KEY_0 /root/lircd.conf.conf
	0000000000ffe01f 00 KEY_VOLUMEDOWN /root/lircd.conf.conf
	0000000000ffe01f 00 KEY_VOLUMEDOWN /root/lircd.conf.conf
	0000000000ff30cf 00 KEY_1 /root/lircd.conf.conf
	0000000000ff18e7 00 KEY_2 /root/lircd.conf.conf
	0000000000ff18e7 01 KEY_2 /root/lircd.conf.conf
	0000000000ff6897 00 KEY_0 /root/lircd.conf.conf
	0000000000ff6897 00 KEY_0 /root/lircd.conf.conf
	0000000000ff38c7 00 KEY_5 /root/lircd.conf.conf
	0000000000ff38c7 01 KEY_5 /root/lircd.conf.conf
	0000000000ff22dd 00 KEY_PREVIOUS /root/lircd.conf.conf
	0000000000ff22dd 00 KEY_PREVIOUS /root/lircd.conf.conf
	0000000000ff52ad 00 KEY_9 /root/lircd.conf.conf
	0000000000ff52ad 01 KEY_9 /root/lircd.conf.conf
	0000000000ff4ab5 00 KEY_8 /root/lircd.conf.conf
	0000000000ff4ab5 01 KEY_8 /root/lircd.conf.conf
	0000000000ff42bd 00 KEY_7 /root/lircd.conf.conf


There's a reason it looks a bit erratic: Some buttons actually caused events not of the button being pushed; for example pushing the "6" button gives KEY_PREVIOUS, normally caused by the "<<" button.

Oddly, there is no lirc.conf.conf in /root. With the help of `find / -type f -name "\*lircd\*"` I did find my `/etc/lirc/lircd.conf` from several months ago when I copied it from the internet. lirc is the ["Linux Infrared Remote Control"](http://www.lirc.org/html/lircd.html), which decodes the infrared signals and provides a unix socket interface to read them from.

`/etc/lirc/lircd.conf`:

	begin remote

	  name  /root/lircd.conf.conf
	  bits           16
	  flags SPACE_ENC|CONST_LENGTH
	  eps            30
	  aeps          100

	  header       9037  4486
	  one           598  1636
	  zero          598   542
	  ptrail        608
	  repeat       9038  2214
	  pre_data_bits   16
	  pre_data       0xFF
	  gap          140796
	  toggle_bit_mask 0x7878

	      begin codes
		  KEY_CHANNELDOWN          0xA25D
		  KEY_CHANNELUP            0xE21D
		  KEY_PREVIOUS             0x22DD
		  KEY_NEXT                 0x02FD
		  KEY_PLAYPAUSE            0xC23D
		  KEY_VOLUMEDOWN           0xE01F
		  KEY_VOLUMEUP             0xA857
		  KEY_EQUAL                0x906F
		  KEY_0                    0x6897
		  KEY_1                    0x30CF
		  KEY_2                    0x18E7
		  KEY_3                    0x7A85
		  KEY_4                    0x10EF
		  KEY_5                    0x38C7
		  KEY_6                    0x5AA5
		  KEY_7                    0x42BD
		  KEY_8                    0x4AB5
		  KEY_9                    0x52AD
	      end codes
	end remote

It appears that since FF prepends all the codes, we only need to put the last 4 hex digits in the config.
In the specific case of "6" being seen as "<<", it must mean 5AA5 is being seen as 22DD which does not seem likely. It could also be that the specific remote I have is somewhat dodgy or faulty.

So clearly something is up and we need to investigate further and gain a better understanding of what lircd is doing.

## lircd and config files
[This post](https://www.hackster.io/austin-stanton/creating-a-raspberry-pi-universal-remote-with-lirc-2fd581) is more or less the same track as what we want to do. It even has the exact same remote with "Car MP3" at the bottom.

I did the process of using `irrecord -d /dev/lirc0 ~/lircd.conf` to generate a config file, and got a slightly different one from the above post:

	begin remote

	  name  /home/me/lircd.conf
	  bits           16
	  flags SPACE_ENC|CONST_LENGTH
	  eps            30
	  aeps          100

	  header       9063  4542
	  one           544  1697
	  zero          544   590
	  ptrail        543
	  pre_data_bits   16
	  pre_data       0xFF
	  gap          141246
	  toggle_bit_mask 0x0

	      begin codes
		  KEY_NEXT                 0x02FD
		  KEY_CHANNELDOWN          0xA25D
		  KEY_CHANNELUP            0xE21D
		  KEY_CHANNEL              0x629D
		  KEY_PREVIOUS             0x22DD
		  KEY_PLAYPAUSE            0xC23D
		  KEY_VOLUMEDOWN           0xE01F
		  KEY_VOLUMEUP             0xA857
		  KEY_EQUAL                0x906F
		  KEY_0                    0x6897
		  KEY_1                    0x30CF
		  KEY_2                    0x18E7
		  KEY_3                    0x7A85
		  KEY_4                    0x10EF
		  KEY_5                    0x38C7
		  KEY_6                    0x5AA5
		  KEY_7                    0x42BD
		  KEY_8                    0x4AB5
		  KEY_9                    0x52AD
	      end codes

	end remote

However, the hex codes are all the same and it still suffers from the issue of '6' causing '<<', the unbound '100+' button causing '-' (volume down), '4' causing '0', and a couple of other mismappings.

At this point I replaced my remote with another from the package of 5 I received, and it had identical issues. So either both remotes are bad (not impossible, manufacturing defects often occur in batches), or the config file is still flawed.

I tried again, but started with the number buttons first and didn't press the 100+ and 200+ buttons at all (as lirc does not appear to have specific bindings for them):

	begin remote

	  name  ./2018-05-13-lircd-try2.conf
	  bits           16
	  flags SPACE_ENC|CONST_LENGTH
	  eps            30
	  aeps          100

	  header       8998  4518
	  one           559  1675
	  zero          559   570
	  ptrail        560
	  pre_data_bits   16
	  pre_data       0xFF
	  gap          141067
	  toggle_bit_mask 0x0

	      begin codes
		  KEY_9                    0x52AD
		  KEY_8                    0x4AB5
		  KEY_7                    0x42BD
		  KEY_6                    0x5AA5
		  KEY_5                    0x38C7
		  KEY_4                    0x10EF
		  KEY_3                    0x7A85
		  KEY_2                    0x18E7
		  KEY_1                    0x30CF
		  KEY_0                    0x6897
		  KEY_VOLUMEUP             0xA857
		  KEY_VOLUMEDOWN           0xE01F
		  KEY_EQUAL                0x906F
		  KEY_PLAYPAUSE            0xC23D
		  KEY_NEXT                 0x02FD
		  KEY_PREVIOUS             0x22DD
		  KEY_CHANNEL              0x629D
		  KEY_CHANNELUP            0xE21D
		  KEY_CHANNELDOWN          0xA25D
	      end codes

	end remote


Unfortunately, the same issues persisted.

I started googling around for other lirc configs for this remote.
First I tried [this one](https://github.com/sdiemer/mpc-lirc/blob/master/lircd.conf) in a mpc-lirc project. Alas, same issues. I started to question if `irw` was reporting the correct values here.

I then decided it was time to reduce the problem to the simplest examples. So I deleted all but the numbers 0 to 9 in the config file and then ran irw. However, buttons like KEY_PLAYPAUSE or KEY_VOLUMEDOWN were still showing up. **Oops**, we probably need to reload LIRC in some way.

`systemctl restart lirc`
`irw`

And now all the number buttons correspond to their correct values! The other buttons do not, of course, do anything, because I deleted their mappings. 

So I restored the original config I generated with irrecord, and it works excellently.


## Next
Now that the remote works, it of course follows to do something with it. It seems common to use the Python library for lirc, altough lirc also seems to have some built in ways like irexec to execute programs when a button is pressed.

The "Car MP3" remote is obviously well suited to controlling music playback. It also seems like it would be suited for video playback / Kodi type work as well, with some creative key binding.
