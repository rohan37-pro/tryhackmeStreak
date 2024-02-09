import time
import utils
import json
import platform


### loading user configs ###
with open("./configs/userConfig.json", 'r') as file:
    users = json.load(file)

if platform.system() == "Windows":
    utils.auto_connect_wifi()



for usr in users:
    if utils.check_today(users[usr]["date"]):
        continue
    driver = utils.get_driver(usr)

    if users[usr]["login"] == False:
        utils.login(driver)
        users[usr]["login"] = True
        with open("./configs/userConfig.json", 'w') as file:
            json.dump(users, file, indent=4)
    pointer = users[usr]["pointer"]
    utils.submit_flag(driver, users, usr)
