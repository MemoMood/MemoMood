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


class MemoMoodLocalSiteTest(StaticLiveServerTestCase):
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

    def setUpAddPlace(self, place):
        self.browser.get('%s%s' % (self.live_server_url, '/mood/add_place'))
        self.browser.find_element(
            By.XPATH, '//*[@id="default-input"]').send_keys(place)
        self.browser.find_element(
            By.XPATH, '/html/body/div/form/button').click()

    def setUpAddPeople(self, people):
        self.browser.get('%s%s' % (self.live_server_url, '/mood/add_people'))
        self.browser.find_element(
            By.XPATH, '//*[@id="default-input"]').send_keys(people)
        self.browser.find_element(
            By.XPATH, '/html/body/div/form/button').click()

    def setUpRecord(self, place, text):
        self.browser.get('%s%s' % (self.live_server_url, '/mood/record'))
        # add place and people
        self.setUpAddPlace(place)
        # start record
        self.browser.find_element(By.ID, 'record-time').send_keys(
            (datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime(f"%d%m%Y%H%M%p"))
        Select(self.browser.find_element(
            By.ID, 'place')).select_by_value(place)
        weather_num = random.randint(1, 6)
        self.browser.find_element(
            By.XPATH, f'//*[@id="default-radio-{weather_num}"]').click()
        self.browser.find_element(
            By.XPATH, '//*[@id="message"]').send_keys(text)
        self.browser.find_element(
            By.XPATH, '/html/body/div/form/div/div[2]/div[6]/button').click()
        self.browser.get('%s%s' % (self.live_server_url, '/mood'))

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
        self.browser.get('%s%s' % (self.live_server_url, '/mood/record'))
        # add place and people
        self.setUpAddPlace('university')
        self.setUpAddPeople('Angle')
        # start record
        time_input = self.browser.find_element(By.ID, 'record-time')
        time_input.send_keys((datetime.datetime.now(
        ) - datetime.timedelta(minutes=5)).strftime(f"%d%m%Y%H%M%p"))
        choose_place = Select(self.browser.find_element(By.ID, 'place'))
        choose_place.select_by_value('university')
        # choose_friend = self.browser.find_element(By.XPATH, '//*[@id="checkbox-item-bell"]')
        # choose_friend = self.browser.find_element(
        #     By.XPATH, '//*[@id="checkbox-item-4"]')
        # choose_friend.click()
        choose_weather = self.browser.find_element(
            By.XPATH, '//*[@id="default-radio-2"]')
        choose_weather.click()
        text_input = self.browser.find_element(By.XPATH, '//*[@id="message"]')
        text_input.send_keys('This is a bad day:(')
        submit_diary = self.browser.find_element(
            By.XPATH, '/html/body/div/form/div/div[2]/div[6]/button')
        submit_diary.click()

    def test_record_total(self):
        self.setUpSignup()
        self.setUpRecord('home', 'Sleepy')
        self.setUpRecord('university', 'Want to go home,')
        self.setUpRecord('market', 'so many people there')
        self.browser.get('%s%s' % (self.live_server_url, '/mood'))
        count_diary = self.browser.find_elements(By.CLASS_NAME, 'shadow-xl')
        self.assertEqual(len(count_diary), 3)

    def test_daily_mood(self):
        self.setUpSignup()
        self.browser.get('%s%s' % (self.live_server_url, '/mood/dailymood'))
        input_a_week = self.browser.find_element(By.ID, 'choose-week')
        input_a_week.send_keys((datetime.datetime.now() - datetime.timedelta(days=7)).strftime(f"%V%Y"))
        submit_week = self.browser.find_element(By.XPATH, '/html/body/div[1]/form/div/button')
        submit_week.click()

    def test_discover_page(self):
        self.setUpSignup()
        self.browser.get('%s%s' % (self.live_server_url, '/mood/discover'))