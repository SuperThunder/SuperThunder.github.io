---
layout: post
title: "RPi Home Server Part 2"
date: 2017-08-08
---

# Miscellaneous Additions while Transmission is Broken
## Adding a regular speedtest
One of the regular parts of Canadian life is getting cheated by your telecoms company. I was getting 10 mb/s instead of 25 last night and realized there must be some time of day that I can get a proper speed, or at the very least the trend in speeds must be interesting.
I (quickly found out)[http://xmodulo.com/check-internet-speed-command-line-linux.html] that a tool called speedtest-cli allows a speedtest to be run from the command line. By running this (*periodically*) from a cronjob, you can easily run regular speed tests. I figured out a decent one liner for the task:

    speedtest-cli > /home/magrat/SpeedTestResults/"speedtest $(date --rfc-3339='seconds')"

or, if you want to see the results as it runs (for testing):

    speedtest-cli | tee /home/magrat/SpeedTestResults/"speedtest $(date --rfc-3339='seconds')"
    
To run the command bihourly I put an entry into the crontab:
(I chose the 47nth minute of every 2nd hour)

    47 */2 * * * speedtest-cli > /home/magrat/SpeedTestResults/"speedtest $(date --rfc-3339='seconds')"

The only thing left to do is build a Python/Bash script to compile all the speedtests into a nice CSV
