import datetime
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.webdriver import WebDriver

class OtherFeaturesTest(StaticLiveServerTestCase):
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

    def test_sleep_time(self):
        self.setUpSignUp(self.account1)
        self.browser.get('%s%s' % (self.live_server_url, '/mood/sleep_time'))
        self.browser.find_element(By.XPATH, '//*[@id="record-time"]').send_keys(datetime.datetime.now().strftime(f"%d%m%Y"))
        sleep_range = self.browser.find_element(By.ID, 'steps-range')
        sleep_range.send_keys(Keys.LEFT)
        sleep_range.send_keys(Keys.LEFT)
        sleep_range.send_keys(Keys.LEFT)
        self.browser.find_element(By.XPATH, '/html/body/div/form/button').click()

    def test_daily_mood(self):
        self.setUpSignUp(self.account1)
        self.browser.get('%s%s' % (self.live_server_url, '/mood/dailymood'))
        input_a_week = self.browser.find_element(By.ID, 'choose-week')
        input_a_week.send_keys((datetime.datetime.now() - datetime.timedelta(days=7)).strftime(f"%V%Y"))
        submit_week = self.browser.find_element(By.XPATH, '/html/body/div[1]/form/div/button')
        submit_week.click()
    
    def test_discover(self):
        self.setUpSignUp(self.account1)
        self.browser.get('%s%s' % (self.live_server_url, '/mood/discover'))
    
    def test_export(self):
        self.setUpSignUp(self.account1)
        self.browser.get('%s%s' % (self.live_server_url, '/mood/export'))
        self.browser.find_element(By.XPATH, '/html/body/div/div/button[1]')
