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
        self.wrong_username = 'aler'
        self.password = 'A'
        self.wrong_password = 'a'

    def check_log_in_wrong_pass(self):
        url = '/'

        self.browser.get(self.site + url)

        popups = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_elements_by_xpath('//div[@class="signin-form"]'))
        username_input = popups[0].find_element_by_xpath('//input[@name="username"]')
        password_input = popups[0].find_element_by_xpath('//input[@name="password"]')

        signup_button = popups[0].find_element_by_xpath('//input[@name="signin"]')

        username_input.send_keys(self.username)
        password_input.send_keys(self.wrong_password)

        signup_button.click()

        assert (self.browser.find_element_by_xpath('//div[@class="signin-content"]'))
        print("wrong password")

    def check_log_in_non_existing_user(self):
        url = '/'

        self.browser.get(self.site + url)

        popups = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_elements_by_xpath('//div[@class="signin-form"]'))
        username_input = popups[0].find_element_by_xpath('//input[@name="username"]')
        password_input = popups[0].find_element_by_xpath('//input[@name="password"]')

        signup_button = popups[0].find_element_by_xpath('//input[@name="signin"]')

        username_input.send_keys(self.wrong_username)
        password_input.send_keys(self.password)

        signup_button.click()

        assert (self.browser.find_element_by_xpath('//div[@class="signin-content"]'))
        print("no such user")

    def check_log_in_all_valid(self):
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

        assert (self.browser.find_element_by_xpath('//div[@name="main_check"]'))
        print("log in is successful")
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
