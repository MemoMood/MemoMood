import time
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver


class MemoMoodSiteTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = WebDriver()
        self.browser.implicitly_wait(10)

    def setUpSignup(self):
        self.browser.get('%s%s' % (self.live_server_url, '/accounts/signup/'))
        self.browser.find_element(By.NAME, "username").send_keys("testcase")
        self.browser.find_element(By.NAME, "email").send_keys("test@gmail.com")
        self.browser.find_element(By.NAME, "password1").send_keys("TCTC0987")
        self.browser.find_element(By.NAME, "password2").send_keys("TCTC0987")
        self.browser.find_element(
            By.XPATH, "//button[text()='Sign Up']").click()

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

    def test_add_place(self):
        self.setUpSignup()
        self.browser.get('%s%s' % (self.live_server_url, '/mood/add_place'))
        input_box = self.browser.find_element(
            By.XPATH, '//*[@id="default-input"]')
        input_box.send_keys('home')
        submit = self.browser.find_element(
            By.XPATH, '/html/body/div/form/button')
        submit.click()

    def test_add_people(self):
        self.setUpSignup()
        self.browser.get('%s%s' % (self.live_server_url, '/mood/add_people'))
        input_box = self.browser.find_element(
            By.XPATH, '//*[@id="default-input"]')
        input_box.send_keys('Bell')
        submit = self.browser.find_element(
            By.XPATH, '/html/body/div/form/button')
        submit.click()

    def test_record_page(self):
        self.setUpSignup()
        self.browser.get('%s%s' % (self.live_server_url, '/mood'))
