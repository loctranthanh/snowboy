import requests
import time

n_try = 3

class ss_request:
    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password
        self.token = ''

    def ss_login(self):
        URL = 'https://sm-api.sunshinetech.vn/api/v1/auth/login'
        PARAMS = {'userName': self.user_name, 'password':self.password}
        HEADERS = {'Content-Type' : 'application/json'}
        result = requests.post(url = URL, params = PARAMS, headers = HEADERS)
        if result.status_code != 200:
            print('login failed!')
            return -1
        else:
            self.token = result.json()['data']['access_token']
            print('login success, token: ' + self.token)
            return 0
    
    def switcher_control(self, device_id, touch_num, status):
        if self.token == '':
            if self.ss_login() == -1:
                return -1
        for i in range(n_try):
            URL = 'https://sm-api.sunshinetech.vn/api/v1/controls/switcher?deviceId=' + device_id + '&switcher=' + str(touch_num) + '&state=' + str(status)
            HEADERS = {'Authorization' : 'Bearer ' + self.token}
            result = requests.get(url = URL, headers = HEADERS)
            if result.status_code != 200:
                if result.status_code == 401:
                    time.sleep(1)
                    self.ss_login()
                    continue
                print(result.status_code)
                return -1
            else:
                return 0