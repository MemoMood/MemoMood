import time
import datetime
import random
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.webdriver import WebDriver


class LogInTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = WebDriver()
        self.browser.implicitly_wait(10)

        self.account1 = {
            'username': 'testcase1',
            'email': 'testcase1@example.com',
            'password': 'TCTC0987',
        }
        self.account2 = {
            'username': 'testcase2',
            'email': 'testcase2@example.com',
            'password': 'TCTC0987',
        }

    def test_login(self):
        self.browser.get('%s%s' % (self.live_server_url, '/accounts/login/'))
        username = self.browser.find_element(By.NAME, "login")
        username.send_keys("natekrth")
        password = self.browser.find_element(By.NAME, "password")
        password.send_keys("Nate12345")
        sign_in_button = self.browser.find_element(
            By.XPATH, "/html/body/div/div/div[4]/form/div[4]/button")
        sign_in_button.click()

    def test_signup(self):
        self.browser.get('%s%s' % (self.live_server_url, '/accounts/signup/'))
        username = self.browser.find_element(By.NAME, "username")
        username.send_keys("test_create")
        email = self.browser.find_element(By.NAME, "email")
        email.send_keys("test@gmail.com")
        password1 = self.browser.find_element(By.NAME, "password1")
        password1.send_keys("test1234")
        password2 = self.browser.find_element(By.NAME, "password2")
        password2.send_keys("test1234")
        sign_up_button = self.browser.find_element(
            By.XPATH, "//button[text()='Sign Up']")
        sign_up_button.click()

    def test_user_not_same(self):
        # sign up first time
        self.browser.get('%s%s' % (self.live_server_url, '/accounts/signup/'))
        self.browser.find_element(By.NAME, "username").send_keys(self.account1['username'])
        self.browser.find_element(By.NAME, "email").send_keys(self.account1['email'])
        self.browser.find_element(By.NAME, "password1").send_keys(self.account1['password'])
        self.browser.find_element(By.NAME, "password2").send_keys(self.account1['password'])
        self.browser.find_element(By.XPATH, "//button[text()='Sign Up']").click()
        # logout
        self.browser.get('%s%s' % (self.live_server_url, '/accounts/logout/'))
        self.browser.find_element(By.XPATH,'/html/body/div/form/div/button').click()
        # sign up again
        self.browser.get('%s%s' % (self.live_server_url, '/accounts/signup/'))
        self.browser.get('%s%s' % (self.live_server_url, '/accounts/signup/'))
        self.browser.find_element(By.NAME, "username").send_keys(self.account1['username'])
        self.browser.find_element(By.NAME, "email").send_keys(self.account1['email'])
        self.browser.find_element(By.NAME, "password1").send_keys(self.account1['password'])
        self.browser.find_element(By.NAME, "password2").send_keys(self.account1['password'])
        self.browser.find_element(By.XPATH, "//button[text()='Sign Up']").click()
        check_warning = self.browser.find_element(By.ID, 'error_1_id_username')
        self.assertNotEqual(check_warning, [])
