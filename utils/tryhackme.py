import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from tqdm import tqdm
import pyperclip
import platform
from datetime import datetime
import subprocess
import json


def get_driver(profile):
    if platform.system() == "Linux":
        option = webdriver.ChromeOptions()
        option.add_argument(f"--user-data-dir=./user-data-dir/{profile}")
        driver = webdriver.Chrome(options=option)
        
    return driver


def wait(t):
    for i in tqdm(range(t)):
        time.sleep(1)

def login(driver) :
    driver.get("https://tryhackme.com/login")
    wait(60)


def submit_flag(driver, users, usr):
    ## constants ##
    input = "//input[@class='form-control room-answer-field']"
    submit = "//div[@class='room-task-input-answer']//button"
    t = datetime.timetuple(datetime.today())
    timef = str(t.tm_mday) + "/" + str(t.tm_mon) + "/" + str(t.tm_year)
    pointer = str(int(users[usr]['pointer']) +1 )

    correct_answer  = True
    while correct_answer:
        with open("./configs/THM_flags.json", 'r') as file:
            flag = json.load(file)
            flag = flag[pointer]
        task_input = flag['task_input']
        print(f"pointer {pointer}, task_input->{task_input}")
        if driver.current_url != flag['link']:
            driver.get(flag['link'])
            time.sleep(3)
        while True:
            try:
                s = f"({submit})[{task_input}]"
                print(f"submit xpath={s}")
                button_e = driver.find_element('xpath', s)
                print(f"button text->{button_e.text.strip()}")
                if button_e.text.strip() in ["Submit", "Completed"]:
                    correct_answer=False
                else:
                    print(f"Flag {pointer} is already submitted")
                    pointer = str(int(pointer)+1)
                print("break", button_e.text)
                break
            except:
                print("exception occure.")
                time.sleep(1)
    print(f"correct answer {correct_answer}")
    print("trying to join room..")
    try:
        driver.find_element('xpath', "//button[@class='btn btn-success btn-sm float-right join-btn']").click()
        wait(10)
    except:
        print("already joined..")
    
    print("searching for the card to expand")
    num_cards = len(driver.find_elements('xpath', "//div[@class='card']"))
    tasks = 0
    for i in range(num_cards):
        tasks += len(driver.find_elements('xpath', f"(//div[@id='task-{i}'])//div[@class='room-task-input']"))
        print(f"{i}total tasks --> {tasks}")
        if tasks >= task_input:
            print(f"found at task-card number {i}")

            elem = driver.find_element('xpath', f"//div[@href='#collapse{i}']")
            if elem.get_attribute("aria-expanded") == "false":
                chain = ActionChains(driver)
                chain.move_to_element(elem).pause(1).click().perform()
            break

    time.sleep(2)
    
    if flag["input"] :
        input = f"({input})[{task_input}]"
        element = driver.find_element("xpath", input)
        element.send_keys(flag["answer"])
        time.sleep(2)
    submit = f"({submit})[{task_input}]"
    driver.find_element("xpath", submit).click()
    users[usr]["pointer"] = pointer
    users[usr]["streak_count"] += 1
    users[usr]["date"] = timef
    
    with open("./configs/userConfig.json", 'w') as file:
        json.dump(users, file, indent=4)

    wait(20)



def check_today(d):
    t = datetime.timetuple(datetime.today())
    timef = str(t.tm_mday) + "/" + str(t.tm_mon) + "/" + str(t.tm_year)
    if d == timef:
        return True
    else:
        return False

def check_wifi_state():
    state = subprocess.run('netsh wlan show interfaces | findstr /r "State"', stdout=subprocess.PIPE, text=True, shell=True)
    state = state.stdout.strip().split(":")[1].strip()
    if state=='connected':
        return True
    else:
        return False

def available_wifi( profiles ):
    available = subprocess.run('netsh wlan show networks | findstr "SSID"', stdout=subprocess.PIPE, text=True, shell=True)
    available = available.stdout.strip().split('\n')
    av = []
    for i in available:
        av.append(i.split(':')[1].strip())

    available= []
    for i in av:
        if i in profiles:
            available.append(i)
    return available


def auto_connect_wifi():
    ## check if already connected
    'netsh wlan show networks | findstr /I "ssid"'
    profile = subprocess.run('netsh wlan show profiles | findstr ":"', stdout=subprocess.PIPE, text=True, shell=True)
    profile = profile.stdout.strip().split("\n")[1:]
    profiles = [ i.split(':')[1].strip() for i in profile]

    
    while check_wifi_state()==False:
        list_wifi = available_wifi(profiles)
        if list_wifi==[]:
            print("no wifi available...")
            wait(30)
            print("rechecking...")
        else:
            for wifi in list_wifi:
                con = subprocess.run(f'netsh wlan connect ssid="{wifi}" name="{wifi}" interface="Wi-Fi"', stdout=subprocess.PIPE, text=True, shell=True)
                print(f"trying to connect to {wifi}")
                wait(10)
                if check_wifi_state()==False:
                    print("connection failed..")
                    continue
                else:
                    break