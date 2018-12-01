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

        self.username = 'alercelik'
        rand =  random.randint(1000, 9999)
        self.password = 'A'

    def check_vote_like(self):
        url = '/'
        self.browser.get(self.site + url)
        popups = WebDriverWait(self.browser, self.delay).until(
	lambda x: x.find_elements_by_xpath('//div[@class="signin-form"]'))
        username_input = popups[0].find_element_by_xpath('//input[@name="username"]')
        password_input = popups[0].find_element_by_xpath('//input[@name="password"]')
                         
        signup_button = popups[0].find_element_by_xpath('//input[@name="signin"]')
                         
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        signup_button.click()
        self.browser.find_element_by_xpath('//a[@name="like"]').click()
        assert (self.browser.find_element_by_xpath('//div[@class="forchecking"]'))
        print("voting like is successful")
	
    def check_vote_dislike(self):
        url = '/'
        self.browser.get(self.site + url)
        self.browser.find_element_by_xpath('//a[@name="dislike"]').click()
        assert (self.browser.find_element_by_xpath('//div[@class="forchecking"]'))
        print("voting dislike is successful")
        
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
