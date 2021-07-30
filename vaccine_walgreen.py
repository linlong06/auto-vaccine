from selenium import webdriver
import time
import pandas as pd
import os
from twilio.rest import Client

df_cities = pd.read_excel('bay area cities.xlsx', sheet_name = 'Sheet2')
list_cities = df_cities['Name'].tolist()

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

driver_path = os.environ['CHROME_DRIVER_PATH']
url = 'https://www.walgreens.com/findcare/vaccination/covid/19/landing'
dob = os.environ['DOB']

options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
options.add_argument("--disable-popup-blocking")
web = webdriver.Chrome(executable_path = driver_path, options = options)

def vaccine_tracking(cycle = 1, interval = 1):
    web.get(url) 
    
    for i in range(cycle):
        time.sleep(interval)
        for city in list_cities:
            location_input = web.find_element_by_xpath('//*[@id="inputLocations"]')
            dob_input = web.find_element_by_xpath('//*[@id="userDob"]')
            q1 = web.find_element_by_xpath('//*[@id="dose1"]')
            q2 = web.find_element_by_xpath('//*[@id="radio-1"]')
            
            location_input.clear()
            location_input.send_keys(city + ", CA")
            dob_input.send_keys(dob)
            q1.click()
            q2.click()
            
            submit = web.find_element_by_xpath('//*[@id="nextBtn"]')
            submit.click()
            
            time.sleep(5)
            
            try:
                result = web.find_element_by_xpath('//*[@id="wag-body-main-container"]/section[1]/section/section/section/section[2]/section/p')
                t = time.localtime()
                if ("with available appointments" in result.text):
                    client.messages.create(
                                          body= str(time.strftime("%H:%M:%S", t)) + ' [Walgreen]: ' + result.text,
                                          from_= os.environ['TWILIO_PHONE_NUMBER'],
                                          to= os.environ['PERSONAL_PHONE_NUMBER']
                                      )
                web.back()
            except:
                continue
        
    web.close()
    print ("Query Completed!")
    
def main():    
    try: 
        vaccine_tracking(5, 1)
    except:
        print ("Error!")


if __name__ == "__main__":
    main()
    
    
