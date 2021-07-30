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
url = 'https://www.cvs.com/vaccine/intake/store/covid-screener/covid-qns'
dob = os.environ['DOB']

options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
options.add_argument("--disable-popup-blocking")
web = webdriver.Chrome(executable_path = driver_path, options = options)

def check_popup(web):
    content = web.find_element_by_tag_name('body')
    if ('survey' in content.text):
        dismiss = web.find_element_by_xpath('//*[@id="acsMainInvite"]/div/a[1]')
        dismiss.click()

def landing_page(web):
    time.sleep(1)
    check_popup(web)
    appointment = web.find_element_by_xpath('//*[@id="box_hero"]/div/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/p[1]/a')
    appointment.click()    
    
def question1_page(web):
    time.sleep(1)
    check_popup(web)
    q1 = web.find_element_by_xpath('//*[@id="questionnaire"]/section/div[2]/div[1]/fieldset/div/div[2]/label')
    q2 = web.find_element_by_xpath('//*[@id="questionnaire"]/section/div[2]/div[2]/fieldset/div/div[2]/label')
    q3 = web.find_element_by_xpath('//*[@id="questionnaire"]/section/div[2]/div[3]/fieldset/div/div[2]/label')
    button = web.find_element_by_xpath('//*[@id="content"]/div[3]/button')
    q1.click()
    q2.click()
    q3.click()
    button.click()

def question2_page(web): 
    time.sleep(1)
    check_popup(web)
    q1 = web.find_element_by_xpath('//*[@id="generic"]/section/div[2]/div/fieldset/div/div[1]/label')
    q1.click()
    button = web.find_element_by_xpath('//*[@id="content"]/div[3]/button')
    button.click()
    
def question3_page(web):
    time.sleep(1)
    check_popup(web)
    q1 = web.find_element_by_xpath('//*[@id="jurisdiction"]/option[6]')
    button = web.find_element_by_xpath('//*[@id="content"]/div[3]/button')
    q1.click()
    button.click()
    
def question4_page(web):
    time.sleep(1)
    check_popup(web)
    q1 = web.find_element_by_xpath('//*[@id="dateOfBirth"]')
    button = web.find_element_by_xpath('//*[@id="content"]/div[3]/button')
    q1.send_keys(dob)
    button.click()

def question5_page(web):
    time.sleep(1)
    check_popup(web)
    schedule_button = web.find_element_by_xpath('//*[@id="content"]/div[3]/button')
    schedule_button.click() 
    
def vaccine_tracking(cycle = 1, interval = 1):
    web.get(url)    
    # landing page
    # landing_page(web)        
    # surve page 1: before schedule your vaccine
    question1_page(web) 
    
    result = web.find_element_by_tag_name('body')
    if ("Info we'll ask for" in result.text):
        question4_page(web) 
    else:
        # survey page 2: 
        question2_page(web)    
        # survey page 3:
        question3_page(web)    
        # survey page 4: info we'll ask for
        question4_page(web)  
        
    # survey page 5:
    question5_page(web)
    
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
                continue
            elif ('glitch' in result.text):
                web.back()
            else:
                print (str(time.strftime("%H:%M:%S", t)) + ' [CVS]: ' + city + ' has slot available')
                client.messages.create(
                          body= str(time.strftime("%H:%M:%S", t)) + ': ' + city + ' has slot available!',
                          from_= os.environ['TWILIO_PHONE_NUMBER'],
                          to= os.environ['PERSONAL_PHONE_NUMBER']
                      )
    web.close()
    
def main():    
    for i in range(10):
        try: 
            vaccine_tracking(10, 1)
        except:
            print ("Error in trial No: " + str(i))
            continue


if __name__ == "__main__":
    main()
    
    
