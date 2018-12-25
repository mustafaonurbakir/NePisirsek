import time
import random
import string

import datetime

from flask import Flask, redirect, url_for, request, flash, session, render_template
from  flask_sqlalchemy  import SQLAlchemy
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
class Test(object):
    def __init__(self):
        self.site = 'http://127.0.0.1:5000'
        self.delay = 2  # seconds
         
        self.name = 'john'
        self.surname = 'doe'
        rand =  random.randint(1000, 9999)
        self.username = 'test' + str(rand)
        self.email = 'test' +str(rand) + '@test.com'
        self.password = 'test3'
		
    def check_sign_up_missing_field(self):
        url = '/sign_up'
                #email missing
        self.browser.get(self.site + url)

        popups = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_elements_by_xpath('//div[@class="signup-form"]'))
        name_input = popups[0].find_element_by_xpath('//input[@name="name"]')
        surname_input = popups[0].find_element_by_xpath('//input[@name="your_surname"]')
        username_input = popups[0].find_element_by_xpath('//input[@name="username"]')

        password_input = popups[0].find_element_by_xpath('//input[@name="pass"]')
        repassword_input = popups[0].find_element_by_xpath('//input[@name="re_pass"]')


        signup_button = popups[0].find_element_by_xpath('//input[@name="signup"]')

        name_input.send_keys(self.name)
        surname_input.send_keys(self.surname)
        username_input.send_keys(self.username)

        
        password_input.send_keys(self.password)
        repassword_input.send_keys(self.password)

        signup_button.click()

        assert(self.browser.find_element_by_xpath('//div[@class="signup-content"]'))
        print("missing fields")    
    
    def check_sign_up_mismatch_password(self):
        url = '/sign_up'
                #password 
        self.browser.get(self.site + url)

        popups = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_elements_by_xpath('//div[@class="signup-form"]'))
        name_input = popups[0].find_element_by_xpath('//input[@name="name"]')
        surname_input = popups[0].find_element_by_xpath('//input[@name="your_surname"]')
        username_input = popups[0].find_element_by_xpath('//input[@name="username"]')
        email_input = popups[0].find_element_by_xpath('//input[@name="email"]')
        password_input = popups[0].find_element_by_xpath('//input[@name="pass"]')
        repassword_input = popups[0].find_element_by_xpath('//input[@name="re_pass"]')


        signup_button = popups[0].find_element_by_xpath('//input[@name="signup"]')

        name_input.send_keys(self.name)
        surname_input.send_keys(self.surname)
        username_input.send_keys(self.username)
        email_input.send_keys(self.email)
        
        password_input.send_keys(self.password)
        repassword_input.send_keys('a')

        signup_button.click()

        assert(self.browser.find_element_by_xpath('//div[@class="signup-content"]'))
        print("mismatch password")    
	
    def check_sign_up_all_valid(self):
        url = '/sign_up'
 
        self.browser.get(self.site + url)

        popups = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_elements_by_xpath('//div[@class="signup-form"]'))
        name_input = popups[0].find_element_by_xpath('//input[@name="name"]')
        surname_input = popups[0].find_element_by_xpath('//input[@name="your_surname"]')
        username_input = popups[0].find_element_by_xpath('//input[@name="username"]')
        email_input = popups[0].find_element_by_xpath('//input[@name="email"]')
        password_input = popups[0].find_element_by_xpath('//input[@name="pass"]')
        repassword_input = popups[0].find_element_by_xpath('//input[@name="re_pass"]')

 
        signup_button = popups[0].find_element_by_xpath('//input[@name="signup"]')

        name_input.send_keys(self.name)
        surname_input.send_keys(self.surname)
        username_input.send_keys(self.username)
        email_input.send_keys(self.email)
        
        password_input.send_keys(self.password)
        repassword_input.send_keys(self.password)
 
        signup_button.click()

        assert(self.browser.find_element_by_xpath('//div[@name="main_check"]'))
        print("signed up correctly")    
        self.browser.find_element_by_xpath('//a["log out"]').click()
            
            
    def run(self):
        self.browser = webdriver.Chrome(r'C:\Users\emreb\Desktop\chromedriver.exe')
        for attr in __class__.__dict__:
            if callable(getattr(self, attr)) and attr.startswith('check'):
                try:
                    getattr(self, attr)()
                    print(f"[+] {attr} passed")
 
                except Exception as e:
                    print(f"[-] {attr} failed")
                    print(e)
 
        self.browser.close()
 
 
if __name__ == '__main__':
    test = Test()
    test.run()
