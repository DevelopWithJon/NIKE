from time import sleep, perf_counter
from pyvirtualdisplay import Display 
import concurrent.futures
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from seleniumwire import webdriver
from selenium.webdriver.firefox.options import Options
import re
import random
import names
import requests
import csv
import sys

display = Display(visible=0, size=(800, 600))
display.start()


file = open('proxy.txt', 'r')
proxy = file.readlines()
proxy_list = [x.strip('\n') for x in proxy]


apikey = 'a92ce6ffd9833f2a1a33a1f1ac03c6c0'
sitekey = '6LekUwwTAAAAAHy7txR20ZdcGtD9XQ5-OcBVjJ2Z&co'
form = 'https://sms-activate.ru/en'

class  SNKRS():
    def __init__(self):
        pass        
        #Let select and prepare a proxy IP address to use 
        
    def get_proxy(self, proxy):
        active_proxy = random.choice(proxy)
        print(active_proxy)
        
        try:
            find = r'\d+.\d+.\d+.\d+'
            host = re.findall(find, active_proxy)
            host = str(host[0])
            print(host)
        except:
            if len(host) < 5:
                try:
                    find = r'.*:'
                    host = re.findall(find, active_proxy)
                    host = str(host[0])
                    host = host[0:-1]
                    print(host)
                except:
                    pass
        
        try:
            find = r':\d+'
            port = re.findall(find, active_proxy)
            port = str(port[0])
            port = port[1:]
            print(port)
        except:
            pass
        
        
        try:
            find = r':[a-zA-Z]+'
            user = re.findall(find, active_proxy)
            user = str(user[0])
            user = user[1:]
            print(user)
        except:
            pass
        if len(user) < 11:
            try:
                find = r':[a-zA-Z0-9]+![a-zA-Z0-9]+'
                user = re.findall(find, active_proxy)
                user = str(user[0])
                user = user[1:]
                print(user)
            except:
                pass
        
        try:
            find = r':[a-zA-Z0-9]+$'
            passw = re.findall(find, active_proxy)
            passw = str(passw[0])
            passw = passw[1:]
            print(passw)
        except:
            pass
        
        if user != None and len(user) > 5:
            print('using authentication')
            self.options = {
            'proxy': {
            'http': f'http://{user}:{passw}@{host}:{port}',
            'https': f'https://{user}:{passw}@{host}:{port}',
            'no_proxy': 'localhost,127.0.0.1,dev_server:8080'
            }
        }
        else:
            print('no authentication needed')
            self.options = {
            'proxy': {
                'http': f'http://{host}:{port}',
                'https': f'https://@{host}:{port}',
                'no_proxy': 'localhost,127.0.0.1,dev_server:8080'
                }
            }
        
        return self.options
    
    def get_solution(self):
        print("Getting captcha solution")
        url="http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}".format(apikey,sitekey,form)
        resp = requests.get(url) 
        if resp.text[0:2] != 'OK':
            quit('Error. Captcha is not received')
        captcha_id = resp.text[3:]
        print(captcha_id)
        fetch_url = "http://2captcha.com/res.php?key={}&action=get&id={}".format(apikey,captcha_id)
        for i in range(1, 20):	
            sleep(5) # wait 5 sec.
            resp = requests.get(fetch_url)
            if resp.text[0:2] == 'OK':
                break
        captchasolution = resp.text[3:]
        return captchasolution
        

    # Lets set up a chrome browser with selenium and load our proxy IP
    def get_fox(self, proxy, ): 
        
        use_proxies = "Y"
        options = self.get_proxy(proxy)
        F_options = Options()
        F_options.headless = True
        profile = webdriver.FirefoxProfile()
        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference('useAutomationExtension', False)
        profile.update_preferences()
        desired = DesiredCapabilities.FIREFOX
        gecko_path = "C:/Users/joeyb/OneDrive/Desktop/Python-9-15/geckodriver.exe"
        if use_proxies == 'Y':
            self.drive = webdriver.Firefox(
            firefox_profile=profile,        
            seleniumwire_options=options,
            desired_capabilities=desired, executable_path=gecko_path) 
        else: 
             self.drive = webdriver.Firefox(desired_capabilities=desired, executable_path=gecko_path)
        
        #self.drive = webdriver.Chrome(ChromeDriverManager().install(), seleniumwire_options=options)
        return self.drive
    
    def order_sms(self):
        print("ordering sms")
        for i in range(1, 20):
            site = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key=9b1dcf267A37ccAe7977400d11b4d8eb&action=getNumber&service=ew&forward=0&operator=any&ref=$ref&country=78&phoneException=')
            sleep(10)
            if site.text[0:6] == "ACCESS":
                print('active')
                sms_id = site.text[14:23]
                phone_number = site.text[24:]
                print(phone_number)
                print("ordering sucessful")
                return sms_id, phone_number
                break
        
    
    def activate_sms(self, sms_id):
        print("activating")    
        for i in range(1, 20):
            sleep(5)
            site = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key=9b1dcf267A37ccAe7977400d11b4d8eb&action=setStatus&status=1&id={}&forward=$forward'.format(sms_id))
            if site.text == "ACCESS_READY": 
                print("activation successful")
                return site.text
                break
                
            else: 
                print("no available numbers because: " + site.text)
            
        
    
    def get_sms_code(self, sms_id):
        
        print("getting sms code")
        for i in range(1, 12):
            sleep(10)
            site = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key=9b1dcf267A37ccAe7977400d11b4d8eb&action=getFullSms&id={}'.format(sms_id))
            if site.text[0:4] == "FULL": 
                sms_code = site.text[-6:]
                print("SMS Code is: " + sms_code)
                return sms_code
                break
            else:
                print('error ' + site.text)
        
    
    
    def request_site(self, proxy ):
        
        try:
        
            self.driver = self.get_fox(proxy)
            
    
            self.driver.get("https://www.nike.com/register")
            
            
            sleep(5)
            Fname = names.get_first_name()
            
            Lname = names.get_last_name()
              
        
            BDay = str(random.randrange(1,12)).zfill(2) + str(random.randrange(1,28)).zfill(2) + str(random.randrange(1970,2002))
            
            Email = Fname + '_' + Lname + str(random.randrange(000,999)) + '@drenchkicksultra.com'
            
            order = self.order_sms()
            SMS_ID = order[0]
            Phone_number = order[1]
            Phone_number = Phone_number[2:]
            print(SMS_ID)
            print(Phone_number)
            
            print(Email)
            
            #Email
            self.driver.find_element_by_name('emailAddress').send_keys(Email)
            #Password
            self.driver.find_element_by_name('password').send_keys('Indestruktable1')
            #First Name
            self.driver.find_element_by_name('firstName').send_keys(Fname)
            #Last Name
            self.driver.find_element_by_name('lastName').send_keys(Lname)
            
            
            #DOB
            DOB = self.driver.find_element_by_name('dateOfBirth')
            
    
            self.driver.find_element_by_name('dateOfBirth').click()
            
            action = ActionChains(self.driver)
            
            action.send_keys_to_element(DOB, BDay + Keys.ENTER).perform()
            
            #Male Button find element id from page source code 
            html = self.driver.page_source  
            soup1= BeautifulSoup(html)
            form = soup1.select("div.nike-unite-gender-buttons.gender.nike-unite-component")
    
            form = form[0]
            gender_raw = form.find_all("li")
            gender_raw = gender_raw[0]
            gender_id = str(gender_raw["id"])
            Male = self.driver.find_element_by_xpath('//*[@id="{}"]/input'.format(gender_id))
            Male.send_keys(Keys.ENTER)
    
    
            #submit form
    
            try:
                Join_Us_btn = self.driver.find_element_by_class_name('submitting')
                Join_Us_btn.click()
            except:
                print('no need to submit----------------------')
                pass
            
            sleep(8)
            
            self.driver.get("https://www.nike.com/member/settings")
            
            sleep(8)
            
            activated = self.activate_sms(SMS_ID)
            
            if activated == "ACCESS_READY":
                print(activated)
                
            sleep(2)
            
            #option sub window
            try:
                add_phone = self.driver.find_element_by_xpath('//*[@id="mobile-container"]/div/div/form/div[2]/div[4]/div/div/div/div[2]/button')
                add_phone.send_keys(Keys.ENTER)
            except:
                print('error')
                sleep(5)
                add_phone = self.driver.find_element_by_xpath('//*[@id="mobile-container"]/div/div/form/div[2]/div[4]/div/div/div/div[2]/button')
                add_phone.send_keys(Keys.ENTER)
            
            sleep(1.5)
            
            country_select = self.driver.find_element_by_class_name('country')
            country_select.send_keys('ff')
            
            html = self.driver.page_source  
            soup3 = BeautifulSoup(html, 'lxml')
            sleep(5)
            phone_raw = soup3.find('div', class_ = 'mobileNumber-div')
            phone_refined = phone_raw.find('input')
            phone_refined_id = str(phone_refined['id'])
            
            
            phone_field = self.driver.find_element_by_xpath('//*[@id="{}"]'.format(phone_refined_id))
            phone_field.send_keys(Phone_number)
            
            
            send_code = self.driver.find_element_by_class_name("sendCodeButton") 
            send_code.send_keys(Keys.ENTER)
            
            sleep(5)
            sms_code = self.get_sms_code(SMS_ID)
            
            if sms_code == None:
                send_code = self.driver.find_element_by_class_name("sendCodeButton") 
                send_code.send_keys(Keys.ENTER)
                sms_code = self.get_sms_code(SMS_ID)
            else:
                pass
            
            html = self.driver.page_source
            soup4 = BeautifulSoup(html, 'lxml')
            
            enter_raw = soup4.find_all("input")
            enter_raw = enter_raw[2]
            enter = enter_raw['id']
            
            enter_code = self.driver.find_element_by_xpath('//*[@id="{}"]'.format(enter))
            enter_code.send_keys(sms_code)
            
            check = self.driver.find_element_by_class_name('checkbox') 
            check.click()
            
            html = self.driver.page_source
            soup5 = BeautifulSoup(html, 'lxml')
            
            submit_raw = soup5.find_all("input")
            submit_id = submit_raw[4]
            submit_id = submit_id['id']
            
            submit = self.driver.find_element_by_xpath('//*[@id="{}"]'.format(submit_id))
            submit.click()
            
            sleep(5)
            
            try:
                state = self.driver.find_element_by_xpath('//*[@id="state"]')
                state.send_keys('new jersey')
            except:
                sleep(3)
                state = self.driver.find_element_by_xpath('//*[@id="state"]')
                state.send_keys('new jersey')
            
            city = self.driver.find_element_by_xpath('//*[@id="city"]')
            city.send_keys("Charleston")
            
            zip_code = self.driver.find_element_by_xpath('//*[@id="code"]')
            zip_code.send_keys('29401')
            
            save_btn = self.driver.find_element_by_xpath('//*[@id="mobile-container"]/div/div/form/div[2]/div[7]/div[2]/div[2]/button')
            save_btn.click()
        
        
        
            print(Email)
        
            sleep(5)
            self.driver.quit()
        
            return Email
            
            # Lets use this to loop through all the previous activty equal the amount of emails we load in our data file
        except:
            print('failed to capture')
            print(sys.exc_info()[0])
            sleep(5)
    
            self.driver.quit()
            
        
    def looper(self, proxy):
        
        loop_count = 0
        
        Email_list = []
        
        #print('will you use proxies?: Y/N')
        #use_proxies = input()
        
        for i in range(1):
                
                verified_email = self.request_site(proxy)
                
                if verified_email != None: 
                
                    Email_list.append(verified_email)
                    
                    loop_count += 1
                
                    print('successfully verified ' + str(loop_count) + ' accounts(s)')
                
                sleep(25)
                
        return Email_list
        
        with open('New_Accounts.csv', 'w', newline='') as myfile:
            wr = csv.writer(myfile)
            wr.writerow(Email_list)

def Test(sec):
    print("sleep for 1 sec")
    a = input()
    print(a)
    sleep(sec)
    print('poop')
    return "Done sleeping"



def main():
    start = perf_counter()
    
    a = SNKRS()
    
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        f1 = executor.submit(a.looper, proxy_list)
        sleep(2)
        f2 = executor.submit(a.looper, proxy_list)
        print(f1.result())
        print(f2.result())
        a.looper(proxy_list)
        
    
    print('success')
    
    finish = perf_counter()
    print(f'Process Finished in {round(finish-start,2)} second(s)')


    
if __name__ == '__main__':
    main()
