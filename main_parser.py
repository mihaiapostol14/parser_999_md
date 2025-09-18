from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import NoSuchElementException

from config import USER_AGENT
from helper import (
    Helper,
    ElementChecker,
    DriverHelper
)



class MainParser(Helper):
    def __init__(self,start_page=0, stop_page=0):
        # Initialize Firefox options
        self.options = webdriver.FirefoxOptions()
        self.options.set_preference("general.useragent.override",
                                    USER_AGENT)  # Set custom user agent to avoid detection as a bot
        self.options.set_preference("dom.webdriver.enabled", False)  # Disable WebDriver detection
        self.options.set_preference("intl.accept_languages", 'en-us')  # Set language WebDriver
        self.options.set_preference("dom.webnotifications.enabled", False)  # Disable WebDriver notifications

        self.service = Service(executable_path='GeckoDriver/geckodriver.exe')  # Path to WebDriver

        self.driver = webdriver.Firefox(service=self.service,
                                        options=self.options)  # Create a new instance of the Firefox WebDriver with the specified options

        self.start_page = start_page
        self.stop_page = stop_page
        self.checker = ElementChecker(driver=self.driver)
        self.driver_helper = DriverHelper(driver=self.driver)

        self.get_item_link()


    def get_item_link(self):
        self.random_pause_code(start=1, stop=5)
        for i in range(self.start_page, self.stop_page + 1):
            self.driver_helper.send_by_url(url=f'https://999.md/ro/list/transport/cars?page={i}')
            self.random_pause_code(start=1, stop=5)

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.create_directory(name_directory=self.driver.current_url.split('/')[-1].split('?')[0])
                if self.checker.class_exists(class_name='styles_adlist__3YsgA'):
                    container = self.driver.find_element(By.CLASS_NAME, 'styles_adlist__3YsgA').find_elements(By.TAG_NAME, 'a')

                    for link in container:
                        link = link.get_attribute('href')
                        if 'login?' not in link:
                            if 'booster' not in link:
                                if 'recommendations' not in link:
                                    if 'favorites' not in link:
                                        self.crate_file(
                                            filename=f"{self.driver.current_url.split('/')[-1].split('?')[0]}/{self.driver.current_url.split('/')[-1].split('?')[0]}_Unsorted_link.txt",
                                            mode='a',
                                            data=link
                                        )

            except NoSuchElementException:
                print('element not found')
            if i == self.stop_page:
                return self.driver_helper.close_driver()


def main():
    return MainParser(
        start_page=1,
        stop_page=2
    )


if __name__ == '__main__':
    main()
