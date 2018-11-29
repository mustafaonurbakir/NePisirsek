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
        self.recipe_name = 'testrecipe'
        self.recipe_text = 'lorem ipsulumx<x'

    def check_profile_page(self):
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
        self.browser.find_element_by_xpath('//a[@name="profile"]').click()
        assert (self.browser.find_element_by_xpath('//div[@class="main_profile"]'))
        print("profile page is successful")

    def check_edit_recipe(self):
        self.browser.find_element_by_xpath('//a[@name="edit"]').click()
        popups = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_elements_by_xpath('//div[@class="editrecipe-form"]'))
        recipe_name_input = popups[0].find_element_by_xpath('//input[@name="recipe_name"]')
        recipe_text_input = popups[0].find_element_by_xpath('//textarea[@name="recipe_text"]')
        recipe_name_input.send_keys(self.recipe_name)
        recipe_text_input.send_keys(self.recipe_text)
        edit_recipe_button = popups[0].find_element_by_xpath('//input[@name="edit_recipe"]')
 
        edit_recipe_button.click()
        assert (self.browser.find_element_by_xpath('//div[@class="forchecking"]')) 
        print("editing recipe is successful")

    def check_delete_recipe(self):
        self.browser.find_element_by_xpath('//a[@name="profile"]').click()
        self.browser.find_element_by_xpath('//a[@name="delete"]').click()
        popups = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_elements_by_xpath('//div[@class="deleterecipe-form"]'))
        category_input = popups[0].find_element_by_xpath('//input[@name="confirmation"]')
        category_input.click()
 
        delete_recipe_button = popups[0].find_element_by_xpath('//input[@name="delete_recipe"]')
 
        delete_recipe_button.click()
        assert (self.browser.find_element_by_xpath('//div[@class="forchecking"]')) 
        print("deleting recipe is successful")
	
		                   
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
