from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import timehutLog

import sys
import os
import re
import requests
import json

# chromedriver = '/Users/michael/Python/PythonTools/myTimehutScrapy/chromedriver'
# whereamiImagePath = '/Users/michael/Python/PythonTools/myTimehutScrapy/'

chromedriver = '/Users/puppylpy/Desktop/Python/PythonTools/myTimehutScrapy/chromedriver'
whereamiImagePath = '/Users/puppylpy/Desktop/Python/PythonTools/myTimehutScrapy/'

os.environ["webdriver.chrome.driver"] = chromedriver

# TODO Process pool or Queue to process multitask in the getTimehut main python file

class timehutSeleniumToolKit:

    def __init__(self, headlessFlag):
        __slots__ = ['__driver', 'albumSet']

        # An empty set that used for storing unique album list
        self.albumSet = set()

        if headlessFlag:
            option = webdriver.ChromeOptions()
            option.add_argument('--headless')
            self.__driver = webdriver.Chrome(executable_path=chromedriver, options=option)
        else:
            self.__driver = webdriver.Chrome(executable_path=chromedriver)

    def loginTimehut(self, username, password):
        WebDriverWait(self.__driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "login")))
        desktop_view_div = self.__driver.find_element_by_class_name('login')
        mobile_view_div = self.__driver.find_element_by_class_name('mobile-login')
        is_desktop_view = self.__driver.find_element_by_class_name('login').is_displayed()

        if desktop_view_div is None or mobile_view_div is None:
            timehutLog.logging.error("Desktop view div or mobile view div is missing in login page")
            return False

        if is_desktop_view and desktop_view_div is not None:
            user_field = desktop_view_div.find_element_by_name('user[login]')
            pw_field = desktop_view_div.find_element_by_name('user[password]')
            button = desktop_view_div.find_element_by_class_name('btn-primary')
        else:
            user_field = mobile_view_div.find_element_by_name('user[login]')
            pw_field = mobile_view_div.find_element_by_name('user[password]')
            button = mobile_view_div.find_element_by_class_name('btn-primary')

        user_field.send_keys(username)
        pw_field.send_keys(password)
        button.click()

        return self.isContentPage()

    def whereami(self, str=''):
        return self.__driver.save_screenshot(f'{whereamiImagePath}whereami-{str}.png')

    def fetchTimehutLoginPage(self, url):
        try:
            self.__driver.get(url)
        except ConnectionResetError as e:
            sys.stderr.write(f'Exception: {e}\n')
        except Exception as e:
            sys.stderr.write(f'{e}\n')

    def fetchTimehutContentPage(self, url):
        try:
            self.__driver.get(url)
        except ConnectionResetError as e:
            sys.stderr.write(f'Exception: {e}\n')
        except Exception as e:
            sys.stderr.write(f'{e}\n')

        return self.isContentPage()

    def isContentPage(self):
        try:
            WebDriverWait(self.__driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "dropload-down")))
        except BaseException as e:
            print(e)
            return False
        finally:
            return True

    def scrollDownTimehutPage(self):
        '''
        Scroll down to page button, and check for
        1. the presence of 'dropload-down' element
        2. the status/text change of 'dropload-refresh'
        :return: Boolean for checking whether the scroll is successful or not
        '''
        WebDriverWait(self.__driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "dropload-down")))
        js = 'document.getElementsByClassName("dropload-down")[0].scrollIntoView(true);'
        wait = WebDriverWait(self.__driver, 10)

        # Execute the scrollIntoView
        self.__driver.execute_script(js)

        # Wait for the dropload-down element is loaded
        try:
            WebDriverWait(self.__driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "dropload-down")))
            wait.until(element_contains_text((By.CLASS_NAME, 'dropload-refresh'), 'more'))
        except BaseException as e:
            sys.stderr.write(f'{e}\n')
            return False
        else:
            return True

    def getTimehutRecordedCollectionRequest(self):
        recorded_request_list = []

        for request in self.__driver.requests:
            if request.response and 'event' in request.path:
                # timehutLog.logging.info(request.path)
                # timehutLog.logging.info(f'Header: {request.headers}')
                # timehutLog.logging.info(f'Code: {request.response.status_code}')
                recorded_request_list.append([request.path, request.headers])

        return recorded_request_list

    def replayTimehutRecordedCollectionRequest(self, req_list, before_day=-200):

        res_list = []
        next_flag = False

        for request in req_list:
            regex = r'.*&before\=(\d*).*'
            result = re.match(regex, request[0])

            if result is not None:
                before = int(result.group(1))
            else:
                before = 3000

            print(f'before: {before}, before_day: {before_day}')
            if before >= before_day:
                next_flag = True
            else:
                next_flag = False
                break

            try:
                r = requests.get(url=request[0], headers=request[1], timeout=30)
                r.raise_for_status()
            except requests.RequestException as e:
                timehutLog.logging.error(e)
            else:
                response_body = json.loads(r.text)
                res_list.append(response_body)
                # timehutLog.logging.info(f"Request fired = {response_body}")

        return res_list, next_flag

    def cleanTimehutRecordedRequest(self):
        del self.__driver.requests

    def getTimehutAlbumURLSet(self):
        album_elements = self.__driver.find_elements_by_class_name('swiper-detail-enter')

        for element in album_elements:
            self.albumSet.add(element.get_attribute('href'))

        return self.albumSet

    def getTimehutRecordedMomeryRequest(self):
        recorded_request_list = []

        for request in self.__driver.requests:
            if request.response and 'events/' in request.path:
                # timehutLog.logging.info(request.path)
                # timehutLog.logging.info(f'Header: {request.headers}')
                # timehutLog.logging.info(f'Code: {request.response.status_code}')
                recorded_request_list.append([request.path, request.headers])

        return recorded_request_list

    def replayTimehutRecordedMemoryRequest(self, req_list):
        res_list = []

        for request in req_list:

            try:
                r = requests.get(url=request[0], headers=request[1], timeout=30)
                r.raise_for_status()
            except requests.RequestException as e:
                timehutLog.logging.error(e)
            else:
                response_body = json.loads(r.text)
                res_list.append(response_body)
                # timehutLog.logging.info(f"Request fired = {response_body}")
                # print(f"Request fired = {response_body}")

        return res_list

    # TODO: Use 'partial' instead of this?
    def quitTimehutPage(self):
        self.__driver.quit()

    def getTimehutPageUrl(self):
        return self.__driver.current_url

    def cheatTimehut(self):
        return self.__driver


class element_contains_text(object):
    '''
    It's a extended expected_condition from Selenium default EC
    This is used to capture the condition of whether some element contains certain strings in their innerHTML
    Make sure the element has certain text
    '''
    def __init__(self, locator, string):
        self.locator = locator
        self.string = string

    def __call__(self, driver):
        # Finding the referenced element
        element = driver.find_element(*self.locator)

        if self.string in element.get_attribute('innerHTML'):
            return element
        else:
            return False

print(f"Module {__file__} is loaded...")
