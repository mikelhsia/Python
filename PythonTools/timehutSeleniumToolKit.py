from selenium import webdriver
import os

chromedriver = '/Users/michael/Python/PythonTools/chromedriver'
os.environ["webdriver.chrome.driver"] = chromedriver
whereamiImagePath = '/Users/michael/Python/PythonTools/'

class timehutSeleniumToolKit:

    def __init__(self, headlessFlag):

        if headlessFlag:
            option = webdriver.ChromeOptions()
            option.add_argument('--headless')
            self.__driver = webdriver.Chrome(executable_path=chromedriver, options=option)
        else:
            self.__driver = webdriver.Chrome(executable_path=chromedriver)

    def loginTimehut(self, username, password):
        desktop_view_div = self.__driver.find_element_by_class_name('login')
        mobile_view_div = self.__driver.find_element_by_class_name('mobile-login')
        isDesktopView = self.__driver.find_element_by_class_name('login').is_displayed()

        if isDesktopView:
            userfield = desktop_view_div.find_element_by_name('user[login]')
            pwfield = desktop_view_div.find_element_by_name('user[password]')
            button = desktop_view_div.find_element_by_class_name('btn-primary')
        else:
            userfield = mobile_view_div.find_element_by_name('user[login]')
            pwfield = mobile_view_div.find_elements_by_name('user[password]')
            button = mobile_view_div.find_element_by_class_name('btn-primary')

        userfield.send_keys(username)
        pwfield.send_keys(password)
        button.click()

    def whereami(self, n=1):
        self.__driver.save_screenshot(f'{whereamiImagePath}whereami-{n}.png')

    def checkPageSource(self):
        return self.__driver.page_source

    def fetchTimehutPage(self, url):
        self.__driver.get(url)

    def scrollDownTimehutPage(self, n=1):
        js = f"var q=document.documentElement.scrollTop={10000 * n}"
        self.__driver.execute_script(js)

    def getTimehutMoment(self):
        pass

    def getTimehutCollection(self):
        pass

    def quitTimehutPage(self):
        self.__driver.quit()

# TODO Operations to scroll up/down to add visibility to the window
# TODO Process pool or Queue to process multitask in the getTimehut main python file

