from xml.dom.minidom import Element
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from time import sleep

from creds import user, password, appointment_url

# Constants
chromedriverpath = "./chromedriver"

url = "https://ais.usvisa-info.com/en-ca/niv/users/sign_in"
month_limit = 3
username_id = "user_email"
password_id = "user_password"
terms_id = "policy_confirmed"
submit_xpath = '//*[@id="new_user"]/p[1]/input'

appointment_id = "appointments_consulate_appointment_facility_id"
continue_link = "Continue"
reschedule_xpath = '//h5[normalize-space()="Reschedule Appointment"]'
reschedule_link = "Reschedule Appointment"

date_id = "appointments_consulate_appointment_date"
next_link = "Next"
a_elements = "//a[@href]"


class bot():
    def __init__(self):
        global password
        if password == "":
            password = str(input("Enter password")).strip()

        self.chrome_options = webdriver.ChromeOptions()
        self.prefs = {
            "profile.default_content_setting_values.notifications": 2}
        self.chrome_options.add_experimental_option("prefs", self.prefs)
        self.driver = webdriver.Chrome(
            executable_path=chromedriverpath, options=self.chrome_options)

# TODO: better handling of wait time instead of sleep
    def login(self):
        self.driver.maximize_window()
        self.driver.get(url)
        sleep(2)
        element = self.driver.find_element(By.ID, username_id)
        element.send_keys(user)
        sleep(2)
        element = self.driver.find_element(By.ID, password_id)
        element.send_keys(password)
        sleep(2)
        element = self.driver.find_element(By.ID, terms_id)
        action = ActionChains(self.driver)
        action.move_to_element(element).click(on_element=element).perform()
        sleep(2)
        element = self.driver.find_element(By.XPATH, submit_xpath)
        element.click()
        sleep(5)

    def go_schedule_page(self):
        # element = self.driver.find_element(By.LINK_TEXT, continue_link)
        # element.click()
        # sleep(5)
        # element = self.driver.find_element(By.XPATH, reschedule_xpath)
        # element.click()
        # sleep(5)
        # element = self.driver.find_element(By.LINK_TEXT, reschedule_link)
        # element.click()
        global appointment_url
        self.driver.get(appointment_url)
        sleep(4)

    def check_dates(self, a_ele):
        flag = False
        for elem in a_ele:
            temp = str(elem.get_attribute("text"))
            if temp.isnumeric():
                num = int(temp)
                if num > 0 and num < 32:
                    flag = True
                    break
        return flag

    def check_toronto(self):
        flag = False
        month = 0
        try:
            element = b.driver.find_element(By.ID, appointment_id)
            s = Select(element)
            s.select_by_visible_text("Toronto")
            sleep(2)
            element = b.driver.find_element(By.ID, date_id)
            element.click()

            while month < month_limit:

                a_ele = self.driver.find_elements(By.XPATH, a_elements)
                if self.check_dates(a_ele):
                    flag = True
                    break

                self.driver.find_element(By.LINK_TEXT, next_link)
                sleep(2)
                month += 1

        except:
            print("Error while selecting Toronto date")
            flag = False
        finally:
            print("Toronto date available", flag)
            return flag, month

    def check_halifax(self):
        flag = True
        month = 0
        try:
            element = b.driver.find_element(By.ID, appointment_id)
            s = Select(element)
            s.select_by_visible_text("Halifax")
            element = b.driver.find_element(By.ID, date_id)
            sleep(2)
            element.click()

            while month < month_limit:

                a_ele = self.driver.find_elements(By.XPATH, a_elements)
                if self.check_dates(a_ele):
                    flag = True
                    break

                self.driver.find_element(By.LINK_TEXT, next_link)
                sleep(2)
                month += 1
        except:
            print("Error while selecting halifax date")
            flag = False
        finally:
            print("Halifax date available", flag)
            return flag


if __name__ == "__main__":
    b = bot()
    b.login()

    sleep(2)
    b.go_schedule_page()

    sleep(2)

    # TODO: Add nu

    if b.check_halifax():
        print("Yeah halifax ")

    flag, date = b.check_toronto()
    if flag:
        print("Toronto date available : ", date)
