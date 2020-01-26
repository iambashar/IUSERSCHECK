
import time
import re

from requests import Session
from bs4 import BeautifulSoup as bs

while True:
    # log and settings

    #TODO: Use logger for log features
    f = open("log.txt", "a+")
    #TODO: Use JSON instead of plaintext
    settfile = open("idpass.txt", "r")
    lines = settfile.read()
    dpass = '1234'
    dtime = 5800
    l = lines.split(" ")

    i = 1
    while i:
        try:
            urname = l[(2*i)-2]
            passwd = l[(2*i)-1]
            with Session() as s:
                site = s.get("http://10.220.20.12/index.php/home/loginProcess")
                bs_content = bs(site.content, "html.parser")
                login_data = {"username":urname,"password":passwd}
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
                        if c == 2 or c == 6 :
                            li.append(row[1])
                        c += 1
                    print(li[0])
                    L = ["\n", li[0], li[1]]
                    f.writelines(L)
                    string1 = li[1]
                    m = int(re.search(r'\d+', string1).group())
                    print(m, 'Minutes')
                    if m > dtime:
                        site = s.get("http://10.220.20.12/index.php/home/chPasswordProcess")
                        bs_content = bs(site.content, "html.parser")
                        cpass_data = {"curr_pass": ps, "new_pass": dpass, "conf_pass": dpass}
                        s.post("http://10.220.20.12/index.php/home/chPasswordProcess", cpass_data)
                        f.write(f"Your Password is set to {dpass}")
                except:
                    f.write("The username/password you entered is incorrect.\nTry again...")
        except:
            break
        i += 1
    f.close()
    time.sleep(300)

settfile.close()
#t = input("Press enter to terminate")
