from selenium import webdriver
import time
import pandas as pd
import os
from twilio.rest import Client

df_cities = pd.read_excel('bay area cities.xlsx', sheet_name = 'Sheet3')
list_zipcodes = df_cities['zipcode'].tolist()

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

driver_path = os.environ['CHROME_DRIVER_PATH']
url = 'https://www.mhealthappointments.com/covidappt'

options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
options.add_argument("--disable-popup-blocking")
web = webdriver.Chrome(executable_path = driver_path, options = options)

def vaccine_tracking(cycle = 1, interval = 1):
    web.get(url) 
    time.sleep(5)
    zip_input = web.find_element_by_xpath('//*[@id="covid_vaccine_search_input"]')
    distance_radio = web.find_element_by_xpath('//*[@id="fifteenMile-covid_vaccine_search"]')
    search = web.find_element_by_xpath('//*[@id="covid_vaccine_search_container"]/div/div/button/span/i')
    
    for i in range(cycle):
        time.sleep(interval)
        
        for zipcode in list_zipcodes:
            zip_input.clear()
            zip_input.send_keys(zipcode)
            distance_radio.click()
            search.click()
            
            time.sleep(5)
            t = time.localtime()
            
            try:
                result = web.find_element_by_xpath('//*[@id="covid_vaccine_search_error"]/p')
                if ("no available appointments" in result.text):
                    print ("No availble appointments in " + zipcode)
            except:
                client.messages.create(
                                      body= str(time.strftime("%H:%M:%S", t)) + ' [Safeway]: there is appointments available in ' + str(zipcode),
                                      from_= os.environ['TWILIO_PHONE_NUMBER'],
                                      to= os.environ['PERSONAL_PHONE_NUMBER']
                                  )
        
    web.close()
    print ("Query Completed!")
    
def main():    
    try: 
        vaccine_tracking(2, 1)
    except:
        print ("Error!")


if __name__ == "__main__":
    main()
    
    
