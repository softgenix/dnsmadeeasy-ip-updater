import requests
import datetime
from pathlib import Path
from requests import Request, Session
import json
#Update DNS made easy, so you can use your dynamic ip address to host a website on a home server.
#Python3 script to check current ip address from an external service, then compares the result with the last ip address we
#saved in a file. If the new ip address doesn't match our old ip address we know it has changed. In that case, we
#update DNSmadeEasy's dynamic dns with our new ip address. Then we write the new ip address to a file,
#and log the time/date of the ipaddress change to a file so we can see how often our internet provider changes our ip.
#This script can be invoked from crontab and run as often as you wish. It will only bother DNSmadeEasy when a change is found.
#I run it every 15 mins.
#
#Change path to the Linux or Windows folder where your counter .dat file will live.
data_folder = Path('/home/pi/www/')
last = data_folder / 'lastip.dat'
changelog = data_folder / 'ip_change_log.dat'
current_ip = '' #global var
last_ip = ''    #global var

#Get our current external ip address from one of these 2 sources.

try:
    current_ip = requests.get('https://api.ipify.org')
    print('Our current ip address is:', current_ip)
except:
    print('ipifyd.org is down. Trying ident.me instead.')
    current_ip = requests.get('https://ident.me')
    print('Our current ip address is', current_ip)


try:
    #this routine gets a website ip address from ipstack.com. You'll need a free api key from ipstack.
    #If the ip address doesn't match what we think our current ip is, then we update dnsmadeeasy
    responsex = requests.get('http://api.ipstack.com/you-website.web?{'your_free_ipstack_api_key')
    datax = json.loads(responsex.text)
    datay = datax["ip"]
    #print('DnsMadeEasy says our ip address is',datay)
    if current_ip == datay:
        print('current_ip and DnsMadeEasy agree on DNS.')
    else:
        print('current_ip and datay are DIFFERENT. Update the ip')
except Exception as e:
    print(e)
    pass
#
#Get our last ip address from file lastip.dat
try:
    with open(last, mode='r') as f:
        last_ip = f.read()
        print('Our last ip address was  :', last_ip)
            
except Exception as e:
    print(e)
    try:
        print('lastip.dat was empty. Writing current ip address to lastip.dat')
        with open(last, mode = 'w') as f:
            f.write(str(current_ip))
            f.close
            last_ip = current_ip
    except Exception as e:
        print(e)
        
#Lets see if our ip address has changed. If so, tell dnsmadeeasy about it.


if current_ip == last_ip and current_ip == datay:
    print('Our ip address has not changed. No update was sent to dnsMadeEasy.')

else:
    print('Our ip address has changed. Notifying dnsMadeEasy.')
    try:
        #See DNSMadeEasy to get your username, password, id. 
        # updating website 1
        result1 = requests.get(f'https://cp.dnsmadeeasy.com/servlet/updateip?username=your_user_name&password=your_pw&id=your_id&ip={current_ip}')
        print('DnsMadeEasy says: ',result1)
        #updating website 2                                 
        result2 = requests.get(f'https://cp.dnsmadeeasy.com/servlet/updateip?username=your_user_name&password=your_pw&id=your_id&ip={current_ip}')
        print('DnsMadeEasy says: ',result2)
        #updating website 3
        result3 = requests.get(f'https://cp.dnsmadeeasy.com/servlet/updateip?username=your_user_name&password=your_pw&id=your_id&ip={current_ip}')
        print('DnsMadeEasy says: ',result3)
        #updating website 4
        result4 = requests.get(f'https://cp.dnsmadeeasy.com/servlet/updateip?username=your_user_name&password=your_pw&id=your_id&ip={current_ip}')
        print('DnsMadeEasy says: ',result4)
        #etc
        
    except Exception as e:
        print(e)
        
    try:
        print('Updating our lastip.dat file')
        with open(last, mode = 'w') as f:
            f.write(str(current_ip))
            f.close
        #keep track of how often our DNS changes by logging the date/time of each change.
        print('Logging this update to ip_change_log.dat')
        with open(changelog, mode = 'a') as f:
            f.write(str(datetime.datetime.now())+' >  ' + str(current_ip) + '\n')
            f.close

    except Exception as e:
        print('...',e)
