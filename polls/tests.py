import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options

class MySeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        options = Options()
        options.add_argument('--headless')
        cls.selenium = WebDriver(options=options)
        cls.selenium.implicitly_wait(5)

        User.objects.create_superuser("isard", "isard@isardvdi.com", "pirineus")
        #User.objects.create_user("prova", "prova@prova.com", "pirineus", is_staff=True)


    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_staff_user_appears_and_can_login(self):
        s = self.selenium

        s.get(f"{self.live_server_url}/admin/")
        s.find_element(By.NAME, "username").send_keys("isard")
        s.find_element(By.NAME, "password").send_keys("pirineus")
        s.find_element(By.XPATH, "//input[@value='Log in']").click()
        time.sleep(1)

        s.find_element(By.LINK_TEXT, "Users").click()
        s.find_element(By.LINK_TEXT, "ADD USER").click()
        time.sleep(1)
        s.find_element(By.NAME, "username").send_keys("prova")
        s.find_element(By.NAME, "password1").send_keys("pirineus")
        s.find_element(By.NAME, "password2").send_keys("pirineus")
        s.find_element(By.NAME, "_save").click()
        time.sleep(1)
        s.find_element(By.LINK_TEXT, "prova").click()
        s.find_element(By.NAME, "is_staff").click()
        s.find_element(By.NAME, "_save").click()
        time.sleep(1)
        s.get(f"{self.live_server_url}/admin/")
        time.sleep(1)
        page = s.page_source
        assert "prova" in page

        s.find_element(By.XPATH, "//button[text()='Log out']").click()
        s.get(f"{self.live_server_url}/admin/login/")
        time.sleep(1)
        s.find_element(By.NAME, "username").send_keys("prova")
        s.find_element(By.NAME, "password").send_keys("pirineus")
        s.find_element(By.XPATH, "//input[@value='Log in']").click()
        time.sleep(1)
        s.find_element(By.XPATH, "//button[text()='Log out']").click()
        time.sleep(1)
