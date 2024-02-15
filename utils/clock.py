import time
from datetime import datetime
from tqdm import tqdm

def wait(t):
    for i in tqdm(range(t)):
        time.sleep(1)

def get_date():
    t = datetime.timetuple(datetime.today())
    timef = str(t.tm_mday) + "/" + str(t.tm_mon) + "/" + str(t.tm_year)
    return timef


def check_today(d):
    timef = get_date()
    if d == timef:
        return True
    else:
        return False