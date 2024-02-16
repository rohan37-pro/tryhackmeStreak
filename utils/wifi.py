import subprocess
from utils import clock

class windows:
    def check_wifi_state(self):
        state = subprocess.run('netsh wlan show interfaces | findstr /r "State"', stdout=subprocess.PIPE, text=True, shell=True)
        state = state.stdout.strip().split(":")[1].strip()
        if state=='connected':
            return True
        else:
            return False

    def available_wifi(self, profiles ):
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


    def auto_connect_wifi(self):
        ## check if already connected
        'netsh wlan show networks | findstr /I "ssid"'
        profile = subprocess.run('netsh wlan show profiles | findstr ":"', stdout=subprocess.PIPE, text=True, shell=True)
        profile = profile.stdout.strip().split("\n")[1:]
        profiles = [ i.split(':')[1].strip() for i in profile]

        
        while self.check_wifi_state()==False:
            list_wifi = self.available_wifi(profiles)
            if list_wifi==[]:
                print("no wifi available...")
                clock.wait(30)
                print("rechecking...")
            else:
                for wifi in list_wifi:
                    con = subprocess.run(f'netsh wlan connect ssid="{wifi}" name="{wifi}" interface="Wi-Fi"', stdout=subprocess.PIPE, text=True, shell=True)
                    print(f"trying to connect to {wifi}")
                    clock.wait(10)
                    if self.check_wifi_state()==False:
                        print("connection failed..")
                        continue
                    else:
                        break