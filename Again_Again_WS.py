import time

while True:
    f = open("log.md", "a+")
    from requests import Session
    from bs4 import BeautifulSoup as bs
    import re

    i = 1

    lines = "Hi"


    file = open("idpass.txt", "r")
    lines = file.read()
    dpass = '1234'
    dtime = 5800
    

    l = lines.split(" ")

    while i:
        try:
            un = l[(2*i)-2]
            ps = l[(2*i)-1]
            #print(un, ps)
            with Session() as s:    
                site = s.get("http://10.220.20.12/index.php/home/loginProcess")
                bs_content = bs(site.content, "html.parser")
                login_data = {"username":un,"password":ps}
                s.post("http://10.220.20.12/index.php/home/loginProcess",login_data)
                home_page = s.get("http://10.220.20.12/index.php/home/dashboard")
                soup = bs(home_page.content, "lxml")

                #print(results)

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
                    #f.write(" %d Minutes\n" % m)
                    #check(m)
                    if m > dtime:
                        site = s.get("http://10.220.20.12/index.php/home/chPasswordProcess")
                        bs_content = bs(site.content, "html.parser")
                        cpass_data = {"curr_pass": ps, "new_pass": dpass, "conf_pass": dpass}
                        s.post("http://10.220.20.12/index.php/home/chPasswordProcess", cpass_data)
                        #print("Your Password is set to", dpass)
                        f.write("Your Password is set to %s" % dpass)

                except:
                    f.write("The username/password you entered is incorrect.\nTry again...")
                    #print("The username/password you entered is incorrect.\nTry again...")
        except:
            break
        i += 1
    f.close()
    time.sleep(300)

file.close()
#t = input("Press enter to terminate")
