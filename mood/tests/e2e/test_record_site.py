import datetime
import random
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.webdriver import WebDriver

class RecordTest(StaticLiveServerTestCase):
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

    def setUpSignUp(self, account):
        self.browser.get('%s%s' % (self.live_server_url, '/accounts/signup/'))
        self.browser.find_element(By.NAME, "username").send_keys(account['username'])
        self.browser.find_element(By.NAME, "email").send_keys(account['email'])
        self.browser.find_element(By.NAME, "password1").send_keys(account['password'])
        self.browser.find_element(By.NAME, "password2").send_keys(account['password'])
        self.browser.find_element(By.XPATH, "//button[text()='Sign Up']").click()

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
            (datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime(f"%d%m%Y%I%M%p"))
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


    def test_record_page(self):
        self.setUpSignUp(self.account1)
        self.browser.get('%s%s' % (self.live_server_url, '/mood/record'))
        # add place and people
        self.setUpAddPlace('university')
        self.setUpAddPeople('Angle')
        # start record
        time_input = self.browser.find_element(By.ID, 'record-time')
        time_input.send_keys((datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime(f"%d%m%Y%I%M%p"))
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
        self.setUpSignUp(self.account1)
        self.setUpRecord('home', 'Sleepy')
        self.setUpRecord('university', 'Want to go home,')
        self.setUpRecord('market', 'so many people there')
        self.browser.get('%s%s' % (self.live_server_url, '/mood'))
        count_diary = self.browser.find_elements(By.CLASS_NAME, 'shadow-xl')
        self.assertEqual(len(count_diary), 3)