from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import NoSuchElementException

from config import USER_AGENT
from helper import (
    Helper,
    ElementChecker
)


class ParserItemInfo(Helper):
    def __init__(self,source_file=''):
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

        self.source_file = source_file
        self.checker = ElementChecker(driver=self.driver)

        self.remove_duplicate(
            default=f"{self.source_file.split("/")[0]}/cars_Unsorted_link.txt",
            sorted_filename=f"{self.source_file.split("/")[0]}/cars_Sorted_link.txt",
        )

        self.iter_by_item()


    def send_by_url(self, url):
        """
        Navigates to the specified URL using the web driver.

        Args:
            url (str): The URL to navigate to.

        Raises:
            WebDriverException: If there is an issue with navigating to the URL.
        """
        # Use the web driver to open the specified URL
        self.driver.get(url=url)



    def iter_by_item(self):
        with open(file=self.source_file, mode='r') as file:
            source = file.read()
            for url in source.split():
                self.random_pause_code(start=1, stop=4)
                self.send_by_url(url=url)
                self.get_phone_number()


    def get_phone_number(self):
        self.random_pause_code(start=1, stop=4)

        self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element(By.CLASS_NAME, 'styles_footer__sKQxZ'))
        self.random_pause_code(start=1, stop=11)
        try:
            if self.checker.tag_exists(tag_name='a'):
                for phone in self.driver.find_elements(By.TAG_NAME, 'a'):
                    if 'tel:' in phone.get_attribute('href'):
                        phone_number = phone.get_attribute('href').replace('tel:',' ')

                        self.crate_file(
                            filename=f"{self.source_file.split('/')[0]}/{self.source_file.split('/')[0]}_Unsorted_phone_number.txt",
                            mode='a',
                            data=phone_number
                        )

        except NoSuchElementException:
            self.crate_file(
                filename=f"{self.source_file.split('/')[0]}/{self.source_file.split('/')[0]}_Not_phone_number.txt",
                mode='a',
                data=self.driver.current_url
            )
            self.close_driver()
        self.remove_duplicate(
            default=f"{self.source_file.split('/')[0]}/{self.source_file.split('/')[0]}_Unsorted_phone_number.txt",
            sorted_filename=f"{self.source_file.split('/')[0]}/{self.source_file.split('/')[0]}_Sorted_phone_number.txt",
        )


    def close_driver(self):
        """Close the WebDriver instance and quits the browser.

        This method closes the current window and terminates the WebDriver session.
        """
        self.driver.close()  # Close the current window
        self.driver.quit()  # Quit the WebDriver session and close all associated windows


def main():
    return ParserItemInfo(
        source_file='cars/cars_Sorted_link.txt'
    )


if __name__ == '__main__':
    main()
