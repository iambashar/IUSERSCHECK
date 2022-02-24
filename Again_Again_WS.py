import telnetlib
from time import sleep
from requests import Session
from bs4 import BeautifulSoup as bs
import re
import csv

current_id = 0
flag = False
current_user = ''

HOST = '192.168.0.1'
router_username = b'admin'
router_password = b'admin'

with telnetlib.Telnet(HOST) as tn:
    tn.read_until(b"username:", 2)
    tn.write(router_username + b'\n')
    tn.write(router_password + b'\n')

    sleep(2)
    tn.write(b'wan show connection info\n')

    tn.read_until(b'username=')
    
    current_user =  tn.read_very_eager().decode('ascii').splitlines()[0]
    
    sleep(2)
    tn.write(b'logout\n')

f_idpass = open("idpass.txt", "r")
c_idpass = list(csv.reader(f_idpass))

c = 0 
for idpass in c_idpass:

    un = idpass[0].strip()

    if un == current_user :
        current_id = c
        break
    c += 1

# runs every 5 mins
while True:
    f_idpass = open("idpass.txt", "r")

    router_username = b'admin'
    router_password = b'admin'

    HOST = '192.168.0.1'

    minute_thresh = 5750
    c_usages = []

    c_idpass = list(csv.reader(f_idpass))
    
    minute_limit = 0

    for idpass in c_idpass:

        try:
            un = idpass[0].strip()
            pw = idpass[1].strip()

            # un = l[(2*i)-2]
            # ps = l[(2*i)-1]
            
            with Session() as s:
                site = s.get("http://10.220.20.12/index.php/home/loginProcess")
                bs_content = bs(site.content, "html.parser")
                login_data = {"username":un,"password":pw}
                s.post("http://10.220.20.12/index.php/home/loginProcess",login_data)
                home_page = s.get("http://10.220.20.12/index.php/home/dashboard")
                soup = bs(home_page.content, "lxml")

                table = soup.table

                c = 1
                li = []

                try:
                    table_rows = table.find_all('tr')
                    for tr in table_rows:
                        td = tr.find_all('td')
                        row = [i.text for i in td]
                        if c == 2 or c == 6 or c == 5 :
                            li.append(row[1])
                        c += 1

                    # update list and sort
                    string1 = li[2]
                    string2 = li[1]
                    minute_limit = int(re.search(r'\d+', string2).group())   # limit
                    minute_used = int(re.search(r'\d+', string1).group())    # used minutes
                    print(f'{un}\t\t{minute_used}')

                    minute_thresh = int(.96 * float(minute_limit))
                    c_usages.append([un, pw, minute_limit - minute_used])
                    
                except Exception as e:
                    print (e)
        except:
            continue
    
    print (current_id)
    if int(minute_limit - c_usages[current_id][2]) > minute_thresh:
        current_id = (current_id + 1) % len(c_usages)
        flag = True
        
    else :
        if flag == True :
            username = c_usages[current_id][0]
            password = c_usages[current_id][1]
            print (username)

            with telnetlib.Telnet(HOST) as tn:
                tn.read_until(b"username:", 2)
                tn.write(router_username + b'\n')
                tn.write(router_password + b'\n')

                sleep(2)
                tn.write(b'wan set service ewan_pppoe --protocol pppoe --username ' + username.encode('ascii') + b' --password  ' + password.encode('ascii') + b' --secondConnection sec_conn_dynip\n')
                
                sleep(2)
                tn.write(b'logout\n')
                flag  = False         
        
    sleep(300)

#t = input("Press enter to terminate")
