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

driver_path = "D:\\softwares\\chromedriver_win32\\chromedriver.exe"
url = "https://www.cvs.com/immunizations/covid-19-vaccine"

options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
options.add_argument("--disable-popup-blocking")
web = webdriver.Chrome(executable_path = driver_path, options = options)

def check_popup(web):
    content = web.find_element_by_tag_name('body')
    if ('survey' in content.text):
        dismiss = web.find_element_by_xpath('//*[@id="acsMainInvite"]/div/a[1]')
        dismiss.click()


def vaccine_tracking(url, cycle, interval):
    web.get(url)
    time.sleep(2)
    
    state = web.find_element_by_xpath("//*[text()='California']")
    state.click()
    time.sleep(1)
    appointment = web.find_element_by_xpath('//*[@id="vaccineinfo-CA"]/div/div/div/div[1]/div[2]/div/div/div[2]/div/div[3]/div/p[2]/a')
    appointment.click()
    
    # surve page 0: before schedule your vaccine
    time.sleep(1)
    check_popup(web)
    q0_1 = web.find_element_by_xpath('//*[@id="questionnaire"]/fieldset/section/div[2]/fieldset/div[2]/div[2]/label')
    q0_2 = web.find_element_by_xpath('//*[@id="questionnaire"]/fieldset/section/div[3]/fieldset/div[2]/div[2]/label')
    q0_3 = web.find_element_by_xpath('//*[@id="questionnaire"]/fieldset/section/div[4]/fieldset/div[2]/div[2]/label')
    continue1 = web.find_element_by_xpath('//*[@id="content"]/div[3]/button')
    
    q0_1.click()
    q0_2.click()
    q0_3.click()
    continue1.click()
    
    # survey page 1
    time.sleep(1)
    check_popup(web)
    q1_1 = web.find_element_by_xpath('//*[@id="generic"]/section/div[2]/div/div/div[1]/label')
    q1_1.click()
    continue0 = web.find_element_by_xpath('//*[@id="content"]/div[3]/button')
    continue0.click()
    
    # survey page 2
    time.sleep(1)
    check_popup(web)
    q2_1 = web.find_element_by_xpath('//*[@id="jurisdiction"]/option[6]')
    continue2 = web.find_element_by_xpath('//*[@id="content"]/div[3]/button')
    
    q2_1.click()
    continue2.click()
    
    # survey page 3
    time.sleep(1)
    check_popup(web)
    q3_1 = web.find_element_by_xpath('//*[@id="q1_0"]')
    q3_2 = web.find_element_by_xpath('//*[@id="generic"]/fieldset/section/div[3]/div/div/div[2]/label')
    q3_3 = web.find_element_by_xpath('//*[@id="qconsent"]')
    continue3 = web.find_element_by_xpath('//*[@id="content"]/div[3]/button')
    
    q3_1.send_keys('32')
    q3_2.click()
    q3_3.click()
    continue3.click()
    
    # survey page 4
    time.sleep(1)
    check_popup(web)
    schedule_button = web.find_element_by_xpath('//*[@id="content"]/div[3]/button')
    schedule_button.click()
    
    # seach availability by city or zip code
    time.sleep(1)
    check_popup(web)
    
    for i in range(cycle):
        time.sleep(interval)   
        for city in list_cities:
            check_popup(web)
            location = web.find_element_by_xpath('//*[@id="address"]')
            location.clear()
            location.send_keys(city + ', CA')
            search = web.find_element_by_xpath('//*[@id="generic"]/div/div/div[1]/button')
            search.click()
            
            # print out zip codes that have availability
            time.sleep(2)
            result = web.find_element_by_tag_name('body')
            t = time.localtime()
            if ('sorry' in result.text):
                #print (str(time.strftime("%H:%M:%S", t)) + ': ' + city + ' no availability')
                continue
            elif ('glitch' in result.text):
                #print (str(time.strftime("%H:%M:%S", t)) + ': ' + city + ' technical error')
                web.back()
            else:
                print (str(time.strftime("%H:%M:%S", t)) + ': ' + city + ' has slot available!!!!')
                client.messages.create(
                          body= str(time.strftime("%H:%M:%S", t)) + ': ' + city + ' has slot available!',
                          from_= os.environ['TWILIO_PHONE_NUMBER'],
                          to= os.environ['PERSONAL_PHONE_NUMBER']
                      )
    web.close()
    
    
for i in range(1000):
    time.sleep(10)
    try: 
        vaccine_tracking(url, 100, 10)
    except:
        print (i)
        continue



    
    
