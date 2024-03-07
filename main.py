import time
from utils import tryhackme
from utils import wifi
from utils import clock
import json
import platform


### loading user configs ###
with open("./configs/userConfig.json", 'r') as file:
    users = json.load(file)

if platform.system() == "Windows":
    con = wifi.windows()
    con.auto_connect_wifi()



for usr in users:
    if clock.check_today(users[usr]["date"]):
        print(f"user {usr} is already submitted...")
        continue
    try:
        driver = tryhackme.get_driver(usr)
    except:
        try:
            driver.quit()
            driver.close()
        except:
            pass
        driver = tryhackme.get_driver(usr)

    if users[usr]["login"] == False:
        tryhackme.login(driver, usr)
        users[usr]["login"] = True
        with open("./configs/userConfig.json", 'w') as file:
            json.dump(users, file, indent=4)
    pointer = users[usr]["pointer"]
    try:
        tryhackme.submit_flag(driver, users, usr)
    except Exception as e :
        print(e)
        clock.wait(500)

