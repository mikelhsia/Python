from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import re
import time

chromedriver = '/Users/michael/Python/PythonTools/chromedriver'
os.environ["webdriver.chrome.driver"] = chromedriver
whereamiImagePath = '/Users/michael/Python/PythonTools/'

# TODO Process pool or Queue to process multitask in the getTimehut main python file

class timehutSeleniumToolKit:

    def __init__(self, babyBoy, headlessFlag):
        __slots__ = ['__driver', 'albumSet', 'baby_id']

        # An empty set that used for storing unique album list
        self.albumSet = set()
        self.baby_id = '537776076' if not babyBoy else '537413380'

        if headlessFlag:
            option = webdriver.ChromeOptions()
            option.add_argument('--headless')
            self.__driver = webdriver.Chrome(executable_path=chromedriver, options=option)
        else:
            self.__driver = webdriver.Chrome(executable_path=chromedriver)

    def loginTimehut(self, username, password):
        desktop_view_div = self.__driver.find_element_by_class_name('login')
        mobile_view_div = self.__driver.find_element_by_class_name('mobile-login')
        is_desktop_view = self.__driver.find_element_by_class_name('login').is_displayed()

        if is_desktop_view:
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

        try:
            WebDriverWait(self.__driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "dropload-down")))
        except BaseException:
            return False
        else:
            return True

    def whereami(self, str=''):
        # print(f'current url = {self.__driver.current_url}')
        return self.__driver.save_screenshot(f'{whereamiImagePath}whereami-{str}.png')

    def fetchTimehutPage(self, url):
        return self.__driver.get(url)

    def scrollDownTimehutPage(self):
        '''
        Scroll down to page button, and check for
        1. the presence of 'dropload-down' element
        2. the status/text change of 'dropload-refresh'
        :return: Boolean for checking whether the scroll is successful or not
        '''
        js = 'document.getElementsByClassName("dropload-down")[0].scrollIntoView(true);'
        wait = WebDriverWait(self.__driver, 10)

        # Execute the scrollIntoView
        self.__driver.execute_script(js)

        # Wait for the dropload-down element is loaded
        try:
            WebDriverWait(self.__driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "dropload-down")))
            wait.until(element_contains_text((By.CLASS_NAME, 'dropload-refresh'), 'more'))
        except BaseException:
            return False
        else:
            return True

    def getTimehutMoment(self):
        pass

    def getTimehutCollection(self):
        '''
        id = Column(String(32), primary_key=True)
        baby_id = Column(String(32))
        created_at = Column(Integer)
        updated_at = Column(Integer)
        months = Column(Integer)
        days = Column(Integer)
        content_type = Column(SmallInteger)
        caption = Column(Text)
        :return: collection_list
        '''
        album_elements = self.__driver.find_elements_by_class_name('main-list-item')
        collection_list = list()

        for element in album_elements:
            if len(element.find_elements_by_class_name('swiper-container')) > 0:
                # This is a collection
                date_str = element.find_element_by_tag_name('i').get_attribute('innerText')
                regex = r'(\d*)Y\-(\d*)M\-(\d*).*'
                result = re.match(regex, date_str)
                y = result.group(1)
                m = result.group(2)
                d = result.group(3)

                cid = element.find_element_by_class_name('swiper-slide').get_attribute('data-param')
                baby_id = self.baby_id
                created_at = ''
                updated_at = ''
                months = (int(y) * 12) + int(m)
                days = int(d)
                content_type = 1
                caption = element.find_element_by_class_name('swiper-describe').find_element_by_tag_name('span').get_attribute('innerText')
                # print(f'id = {cid}\n '
                #       f'baby id = {baby_id}\n '
                #       f'months = {months}\n '
                #       f'days = {days} \n '
                #       f'caption = {caption}\n'
                #       f'===================\n')

                collection_list.append([cid, baby_id, created_at, updated_at, months, days, content_type, caption])
            elif len(element.find_elements_by_class_name('text')) > 0:
                # This is a text
                date_str = element.find_element_by_tag_name('i').get_attribute('innerText')
                regex = r'(\d*)Y\-(\d*)M\-(\d*).*'
                result = re.match(regex, date_str)
                y = result.group(1)
                m = result.group(2)
                d = result.group(3)

                cid = element.find_element_by_class_name('text-bottom').get_attribute('data-id')
                baby_id = self.baby_id
                created_at = ''
                updated_at = ''
                months = (int(y) * 12) + int(m)
                days = int(d)
                content_type = 2
                caption = element.find_element_by_class_name('text-content').get_attribute('innerText')
                # print(f'id = {cid}\n '
                #       f'baby id = {baby_id}\n '
                #       f'months = {months}\n '
                #       f'days = {days} \n '
                #       f'caption = {caption}\n'
                #       f'===================\n')

                collection_list.append([cid, baby_id, created_at, updated_at, months, days, content_type, caption])
            elif len(element.find_elements_by_class_name('milestone')) > 0:
                # This is a milestone
                pass
            else:
                # There is something else
                print('[Important]: Missing a type!!')
        else:
            return collection_list

    def getTimehutAlbumURLSet(self):
        album_elements = self.__driver.find_elements_by_class_name('swiper-detail-enter')
        # print(f'no of elements: {len(album_elements)}')

        for element in album_elements:
            # print(f'href: {element.get_attribute("href")}')
            self.albumSet.add(element.get_attribute('href'))

        return len(self.albumSet)

    def quitTimehutPage(self):
        self.__driver.quit()

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
