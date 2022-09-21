import yagmail
import pandas as pd
# Importing os for getting login into the sender mail address by environment password.
import os
import time
sender= 'satyamsingh20942@gmail.com'

# Selenium is used for scraping the value.

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Giving information about the sender mail and password in order to send the mail to reciever.
yag= yagmail.SMTP(user= sender, password= os.getenv('password'))

#This is the subject of the mail address.
subject= "Regarding the stock market exchange percentage"

#In order to work with chromedriver to scrape the value.
service= Service('C:\\Users\\satya\\Downloads\\chromedriver.exe')


def get_drvier():
  # Set options to make browsing easier.
  options = webdriver.ChromeOptions()
  options.add_argument("disable-infobars")
  options.add_argument("start-maximized")
  options.add_argument("disable-dev-shm-usage")
  options.add_argument("no-sandbox")
  options.add_experimental_option('excludeSwitches', ['enable-automation'])
  options.add_argument("disable-blink-features=AutomationControlled")

  driver = webdriver.Chrome(service=service, options=options)
  driver.get("https://zse.hr/en/indeks-366/365?isin=HRZB00ICBEX6")
  return driver

def value(text):
  # Spliting the value which are present on the same xpath so as to get the required value.
  output= str(text.split(" ")[1])
  return output

def hello():
  driver = get_drvier()  
  time.sleep(0.5)
  # Getting the data through xpath.
  element = driver.find_element(by="xpath", value="/html/body/div[2]/div/section[1]/div/div/div[2]")
  return value(element.text)

# req_value= hello()
while True:
 # Checking the stock percentage through the function.
 hello() 
 
 if float(hello())<= -0.10:
   
   #we are reading the information about the reciever through csv file.
   df= pd.read_csv('stock market notification reciever.csv')
   
   for index,row in df.iterrows():
     #content of the mail.
     content= f"""hi!!! {row['name']} the rate is below or equal to -0.10 the current rate is {hello()}"""
     
     #after extracting the detail of the reciever Let's mail them.
     yag.send(to= row['email'], subject= subject, contents= content)
     print('Email sent!')
 
 
 
 #we are giving this sleep time as it will run the loop after certain time so that the reciever did not get mail continuously after each second. This is annoying for the reciever.
 time.sleep(3600)
