from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver

class AddFactorDetailTest(StaticLiveServerTestCase):
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

    def test_add_place(self):
        self.setUpSignUp(self.account1)
        self.browser.get('%s%s' % (self.live_server_url, '/mood/add_place'))
        input_box = self.browser.find_element(
            By.XPATH, '//*[@id="default-input"]')
        input_box.send_keys('home')
        submit = self.browser.find_element(
            By.XPATH, '/html/body/div/form/button')
        submit.click()

    def test_add_people(self):
        self.setUpSignUp(self.account1)
        self.browser.get('%s%s' % (self.live_server_url, '/mood/add_people'))
        input_box = self.browser.find_element(
            By.XPATH, '//*[@id="default-input"]')
        input_box.send_keys('Bell')
        submit = self.browser.find_element(
            By.XPATH, '/html/body/div/form/button')
        submit.click()

    def test_add_mood(self):
        # In selenium, it can't use to click if checkbox is hidden
        pass
