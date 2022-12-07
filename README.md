# dnsmadeeasy-ip-updater
#
#MIT license
#
I wrote this script because I needed to host a raspi on my home internet connection.

It updates DNS settings at DNSmadeeasy.com, so you can use your dynamic ip address to host a website on a home server.

Checks current ip address from an external service, then compares the result with the last ip address we
saved in a file. 

If the new ip address doesn't match our old ip address we know it has changed. In that case, we
update DNSmadeEasy's dynamic dns with our new ip address. Then we write the new ip address to a file,
and log the time/date of the ipaddress change to another file so we can see how often our internet provider changes our ip.

This script can be invoked from crontab and run as often as you wish. 
It will only bother DNSmadeEasy when a change is found. I run it every 15 mins that seems to work very well with my ISP, 
who only changes my address every few months.

DNSMadeEasy has free accounts, but the paid account is well worth it.
I've also found that DnsMadeEasy work nicely with alt domains, such as those supported by OpenNic Project (.bbs, .indy, .gopher, pirate, .geek, etc), 
https://www.opennic.org
