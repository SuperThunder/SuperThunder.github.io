---
layout: post
title: "Controlling the fiery demon inside the Orange Pi Zero 512MB"
date: 2018-04-29
---
## Lockups
On the stock settings for both the 3.4 and 4.* Armbian distributions the H2+ SoC runs quite hot (60C+ normal) and tends to lockup after a few seconds on any intensive task. A large part of this is the 4 cores running as high as 1.2GHz without active cooling. The GPU also remains active even if no display is connected to the TV-out port.

This problem is worse on the Orange Pis sold today as the voltage regulator either puts out 1.1V or 1.3V, with 1.3V tending to cause overheating. So we want to stay at the 1.1V level as much as possible.

## h3consumption
The easiest way to bring some stability is to use h3consumption. For example,
`Disable the GPU: h3consumption -g off`
`Use only 2 cores: h3consumption -c 2`
`Limit the CPU frequency: h3consumption -m 1100`
There is also a fixthermal.sh script on the forums that will do these changes for you.

Unfortunately, h3consumption is not available for the 4.* kernel so I had to go back to 3.4 to have system stability.

These settings alone can bring the orange pi to a thermally stable point. If unused, you can also disable the wifi, ethernet, or USB ports, and limit the RAM frequency.

## Results
With no GPU, 4 cores at max 1008MHz, and 400MHz RAM, my Orange Pi Zero idles around 47C at room temperature
I stress test with a Python script that pegs a single core at 100% quite well:
`#!/usr/bin/env python3

n_limit = int(input("Enter n_limit: "))

def sieve(n):
        primes = []
        # n**2 will not be prime, so n^2 - 1 is largest possible
        max_number = n**2 -1

        # step by each n upto n_limit
        not_prime = []
        # choose number to count up by - 2, 3, 4, 5 etc
        for step in range(2, n_limit):
                # start at the 2*step itself, in case it is prime 
                not_prime += [x for x in range(2*step, max_number, step)]

        # get rid of duplicates
        not_prime = list(set(not_prime))
        #print("Not prime: " + str(not_prime))

        print("Not prime count: " + str(len(not_prime)))

        prime = [p for p in range(1, max_number) if p not in not_prime]

        print("Prime count: " + str(len(prime)))
        #print("\nPrime by filtering: " + str(prime))

sieve(n_limit)`
(don't put in anything above around 150 because it will never finish and probably lock up the pi from running out of memory)

The temperature was stable at a bit below 60C.

## Copper heatsink
Since any kind of enclosure would still cause temperatures to easily rise above 60C, I ordered some small copper heatsinks. This gave a small boost of 2-3C better at load.

On a cool day with the copper heatsink on and 1 core at 100%, I had trouble getting the Pi above 55C

With 3 cores at 100% with the `stress` utility, the CPU temperature quickly rose to 62C and stabilized after a slow climb to 70C. The Pi remained responsive throughout, but it is clear that good cooling would be needed for any intensive use. The USB/audio/TV-out/IR/mic expansion board, while nifty, makes this difficult as it sits about 1cm off the main board.

With 2 cores at 100% with `stress -c 2`, the temperature stabilized at about 67C in open air. With a reasonable heatsink and the right limits it should be possible to use the OPi Zero inside a Gameboy case, and maybe even run multicore emulators.

## Next
One solution for getting a bigger heatsink on while still using the expansion board would be to use male to female pin jumper cables to move the expansion board away. I don't think this would mess up the timing of anything since USB and audio ports on the front panels of computers can have a good foot or two of cable to move through in some cases.


