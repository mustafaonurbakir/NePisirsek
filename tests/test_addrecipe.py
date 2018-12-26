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
        self.password = 'A'

        self.recipe_name = 'testrecipe'
        self.recipe_text = 'lorem ipsulum'

        

    def check_add_recipe_no_ingredient(self):
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

        url = '/add_recipe'
 
        self.browser.get(self.site + url)

        popups = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_elements_by_xpath('//div[@class="addrecipe-form"]'))
        recipe_name_input = popups[0].find_element_by_xpath('//input[@name="recipe_name"]')
        recipe_text_input = popups[0].find_element_by_xpath('//textarea[@name="recipe_text"]')
        recipe_name_input.send_keys(self.recipe_name)
        recipe_text_input.send_keys(self.recipe_text)
        category_input = popups[0].find_element_by_xpath('//input[@name="category"]')
        category_input.click()
        
        add_recipe_button = popups[0].find_element_by_xpath('//input[@name="add_recipe"]')
 
        add_recipe_button.click()
 
        assert (self.browser.find_element_by_xpath('//div[@name="add"]')) 
        print("no ingredient")
        
    def check_add_recipe_no_category(self):
        
        url = '/add_recipe'
 
        self.browser.get(self.site + url)

        popups = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_elements_by_xpath('//div[@class="addrecipe-form"]'))
        recipe_name_input = popups[0].find_element_by_xpath('//input[@name="recipe_name"]')
        recipe_text_input = popups[0].find_element_by_xpath('//textarea[@name="recipe_text"]')
        recipe_name_input.send_keys(self.recipe_name)
        recipe_text_input.send_keys(self.recipe_text)

        ingredient_input = popups[0].find_element_by_xpath('//input[@name="ingredient"]')
        ingredient_input.click()
        
        add_recipe_button = popups[0].find_element_by_xpath('//input[@name="add_recipe"]')
 
        add_recipe_button.click()
 
        assert (self.browser.find_element_by_xpath('//div[@name="add"]')) 
        print("no category")
    def check_add_recipe_all_valid(self):
        
        url = '/add_recipe'
 
        self.browser.get(self.site + url)

        popups = WebDriverWait(self.browser, self.delay).until(
            lambda x: x.find_elements_by_xpath('//div[@class="addrecipe-form"]'))
        recipe_name_input = popups[0].find_element_by_xpath('//input[@name="recipe_name"]')
        recipe_text_input = popups[0].find_element_by_xpath('//textarea[@name="recipe_text"]')
        recipe_name_input.send_keys(self.recipe_name)
        recipe_text_input.send_keys(self.recipe_text)
        category_input = popups[0].find_element_by_xpath('//input[@name="category"]')
        category_input.click()

        ingredient_input = popups[0].find_element_by_xpath('//input[@name="ingredient"]')
        ingredient_input.click()
        
        add_recipe_button = popups[0].find_element_by_xpath('//input[@name="add_recipe"]')
 
        add_recipe_button.click()
 
        assert (self.browser.find_element_by_xpath('//div[@name="main_check"]')) 
        print("adding recipe is successful")
            
            
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
