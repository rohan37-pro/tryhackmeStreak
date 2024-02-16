import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import platform
from datetime import datetime
import json
from utils import clock
import os


def get_driver(profile):
    current_user = os.getlogin()
    option = webdriver.ChromeOptions()
    option.add_argument("--disable-notifications")
    if platform.system() =="Windows":
        option.add_argument(f"--user-data-dir=C:/Users/{current_user}/AppData/Local/Google/Chrome/User Data/tryhackme/{profile}")
        try:
            driver = webdriver.Chrome(executable_path="drivers/chromedriver.exe",options=option)
        except:
            try:
                driver = webdriver.Chrome(options=option)
            except:
                service = Service(executable_path="drivers/chromedriver.exe")
                driver = webdriver.Chrome(service=service, options=option)
    elif platform.system()=="Linux":
        # set this option for linux in order to work on linux 
        # option.add_argument(f"--user-data-dir=/tryhackme/{profile}")  
        driver = webdriver.Chrome(options=option)
    driver.maximize_window()
    return driver

def close_pop_up(driver):
    try:
        driver.find_element('xpath', "//a[@class='cc-btn cc-dismiss']").click()
    except:
        pass
    try:
        alert = driver.switch_to.alert
        alert.dismiss()
    except:
        pass


def join_room(driver):
    try:
        driver.find_element('xpath', "//button[@class='btn btn-success btn-sm float-right join-btn']").click()
        print("joined the room...")
    except:
        pass
    

def login(driver) :
    driver.get("https://tryhackme.com/login")
    currentURL = driver.current_url
    print("Waiting to login... \nPlease login with your credentials.")
    while driver.current_url == currentURL:
        time.sleep(0.5)
    print(f"successfully logged in\n")



def wait_to_load_room(driver):
    print("waiting to load the room...")
    while True:
        try:
            driver.find_element('xpath', "//div[@id='loader']")
            time.sleep(0.5)
        except:
            break



def submit_flag(driver, users, usr):
    ## constants ##
    input = "//input[@class='form-control room-answer-field']"
    submit = "//div[@class='room-task-input-answer']//button"
    timef = clock.get_date()
    pointer = str(int(users[usr]['pointer']) +1 )

    correct_answer  = True
    while correct_answer:
        with open("./configs/THM_flags.json", 'r') as file:
            flag = json.load(file)
            flag = flag[pointer]
        task_input = flag['task_input']
        if driver.current_url != flag['link']:
            driver.get(flag['link'])
            time.sleep(2)

        # check if logged in...
        try:
            driver.find_element('xpath', "(//a[@href='/login'])[1]")
            login(driver)
            driver.get(flag['link'])
            time.sleep(2)
        except:
            pass

        wait_to_load_room(driver)
        join_room(driver)
        close_pop_up(driver)
        while True:
            try:
                s = f"({submit})[{task_input}]"
                button_e = driver.find_element('xpath', s).text.strip().lower()
                while button_e == "join this room":
                    join_room(driver)
                    time.sleep(2)
                    button_e = driver.find_element('xpath', s).text.strip().lower()
                    close_pop_up(driver)

                if button_e in ["submit", "completed"]:
                    correct_answer=False
                else:
                    print(f"Flag {pointer} is already submitted, trying next.")
                    pointer = str(int(pointer)+1)
                break
            except Exception as e:
                close_pop_up(driver)
                print(f"exception occure.\n{e}")
                time.sleep(1)
    
    print("searching for the card to expand")
    num_cards = len(driver.find_elements('xpath', "//div[@class='card']"))
    tasks = 0
    for i in range(1,num_cards+1):
        tasks += len(driver.find_elements('xpath', f"(//div[@id='task-{i}'])//div[@class='room-task-input']"))
        if tasks >= task_input:
            print(f"found at task-card number {i}")
            card = i
            elem = driver.find_element('xpath', f"//div[@href='#collapse{i}']")
            if elem.get_attribute("aria-expanded") == "false":
                chain = ActionChains(driver)
                chain.move_to_element(elem).pause(1).click().perform()
            print("the card has been expanded")
            break

    time.sleep(2)
    ### trying to start machine
    machine = f"//div[@id='task-{card}']//button[@class='btn btn-success']"
    try:
        driver.find_element('xpath', machine).click()
        time.sleep(1)
    except:
        pass
    
    if flag["input"] :
        input = f"({input})[{task_input}]"
        element = driver.find_element("xpath", input)
        chain = ActionChains(driver)
        chain.move_to_element(element).perform()
        element.send_keys(flag["answer"])
        time.sleep(1)
    submit = f"({submit})[{task_input}]"
    but = driver.find_element("xpath", submit)
    chain = ActionChains(driver)
    chain.move_to_element(but).click().perform()
    print("flag has been submitted !!! ")
    users[usr]["pointer"] = pointer
    users[usr]["streak_count"] += 1
    users[usr]["date"] = timef
    
    with open("./configs/userConfig.json", 'w') as file:
        json.dump(users, file, indent=4)
        
    clock.wait(30)

