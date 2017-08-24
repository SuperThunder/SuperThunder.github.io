---
layout: post
title: "RPi Home Server Part 2"
date: 2017-08-08
---

### Miscellaneous Additions while Transmission is Broken
## Adding a regular speedtest
I often find the speed I get downloading from high-speed (ie, much better than my internet) sources is far below what my telecom promises they give me (_ahem_ *Bell Canada*). As the RPi is on 24/7 I realized I could use it to make regular speed tests.
I [quickly found out](http://xmodulo.com/check-internet-speed-command-line-linux.html) that a tool called speedtest-cli allows a speedtest to be run from the command line. By running this (*periodically*) from a cronjob, you can easily run regular speed tests. I figured out a decent one liner for the task:

    speedtest-cli > /home/magrat/SpeedTestResults/"speedtest $(date --rfc-3339='seconds')"

or, if you want to see the results as it runs (for testing):

    speedtest-cli | tee /home/magrat/SpeedTestResults/"speedtest $(date --rfc-3339='seconds')"
    
To run the command bihourly I put an entry into the crontab:
(I chose the 47nth minute of every 2nd hour)

    47 */2 * * * speedtest-cli > /home/magrat/SpeedTestResults/"speedtest $(date --rfc-3339='seconds')"

To compile the results into a nice CSV I wrote a simple Python script:

    # Python 3

    from os import listdir
    from os.path import isfile, join
    import re

    def main():
        CSV_Rows = []
        files_InDir = [f for f in listdir('./') if isfile(join('./', f)) ]
        files_InDir.sort() # sort so they get properly arranged by datetime
        SpeedTest_Filenames = [f for f in files_InDir if 'speedtest ' in f]

        #print(SpeedTest_Filenames)
        
        # loop through the speedtest files, open the text file content
        # find the download and upload lines, figure out the datetime from the filename
        for fname in SpeedTest_Filenames:
            #print(fname)
            with open(fname, 'r') as speedtest_file:
                SpeedTest_Text = speedtest_file.read()
                #lines = speedtest_file.read().split('\n')
                Download_Regex = "Download: \d+\.\d+.*\n"
                Upload_Regex = "Upload: \d+\.\d+.*\n*" # Have to match 0 or more newlines at the end since Upload speed tends to have EOF right after the Mbits/s
                # Search for the download speed result
                try:
                    # Take the first search result; there should only be one anyway
                    Download_Search = re.search(Download_Regex, SpeedTest_Text).group(0)
                    # Strip out the 'Download: ' part
                    # This way only gives the number, not the unit
                    Download_Search = Download_Search.split(' ')[1]
                    # If you want the Mbits/s included
                    #Download_Search = Download_Search.split(' ')[1::]
                    #Download_Search = ' '.join(Download_Search).strip('\n')
                    #print('Download: %s'%Download_Search)
                except AttributeError:
                    print('No download speed for %s'%fname)
                    Download_Search = ''

                # Search for the upload speed
                try:
                    Upload_Search = re.search(Upload_Regex, SpeedTest_Text).group(0)
                    Upload_Search = Upload_Search.split(' ')[1]
                    #print('Upload: %s'%Upload_Search)
                except AttributeError:
                    print('No upload speed for %s'%fname)
                    Upload_Search = ''

            SpeedTest_Datetime = ' '.join( fname.split(' ')[1::] )
            print('%s\tDown: %s\tUp: %s'%(SpeedTest_Datetime,Download_Search,Upload_Search))
            CSV_Rows.append( [SpeedTest_Datetime, Download_Search, Upload_Search] )

        # Output the data to a CSV
        Header = ['Datetime', 'Down (Mbits/s)', 'Up (Mbits/s)']
        WriteToCSV('Bandwidth Test Results.csv', CSV_Rows, Header)

            
    def WriteToCSV(Name, Data, Header):
        import csv
        with open(Name, 'w', newline='') as output_file:
            writer = csv.writer(output_file)
            if(Header is not None):
                writer.writerow(Header)

            for entry in Data:
                writer.writerow(entry)

                              
    main()


Which outputs a nice CSV like this (sample):

    Datetime	    Down (Mbits/s)	    Up (Mbits/s)
    2017-08-08 16:47:01-04:00	29.47	6.97
    2017-08-08 17:47:01-04:00	30.23	7.06
    2017-08-08 18:47:01-04:00	21.24	6.66
    2017-08-08 19:47:01-04:00	25.09	6.68
    2017-08-08 20:47:01-04:00	30.1	7.04
    2017-08-08 21:47:02-04:00	30.41	7.07
    2017-08-08 22:47:01-04:00	29.24	6.85


In the future, I also want to check if going through a VPN changes the speedtest results significantly (as ISPs tend to make speedtests go much faster than normal traffic these days). Smart people before me have [already done such analyses](https://tomrichards.net/2014/04/my-isp-is-cheating-on-speed-tests-too/), typically with the result that when they use a less well known speedtest service, go through a VPN, or use a high bandwidth service like Netflix/Steam/Microsoft/Google their speed is much lower than what the ISP and popular speedtests claim.
