from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import NoSuchElementException

from config import USER_AGENT
from helper import Helper


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

        self.get_item_link()

    def xpath_exists(self, xpath):
        """Checks if an element with the given XPath exists on the page.

        Args:
            xpath (str): The XPath of the element to check.

        Returns:
            bool: True if the element exists, False otherwise.
        """
        try:
            # Attempt to find the element by XPath
            self.driver.find_element(By.XPATH, xpath)
            exist = True
        except NoSuchElementException:
            # If NoSuchElementException is raised, the element does not exist
            exist = False
        return exist

    def id_exists(self, element_id):
        """Checks if an element with the given ID exists on the page.

        Args:
            element_id (str): The ID of the element to check.

        Returns:
            bool: True if the element exists, False otherwise.
        """
        try:
            # Attempt to find the element by XPath
            self.driver.find_element(By.ID, element_id)
            exist = True
        except NoSuchElementException:
            # If NoSuchElementException is raised, the element does not exist
            exist = False
        return exist

    def class_exists(self, class_name):
        """Checks if an element with the given class name exists on the page.

        Args:
            class_name (str): The class name of the element to check.

        Returns:
            bool: True if the element exists, False otherwise.
        """
        try:
            # Attempt to find the element by class name
            self.driver.find_element(By.CLASS_NAME, class_name)
            exist = True
        except NoSuchElementException:
            # If NoSuchElementException is raised, the element does not exist
            exist = False
        return exist

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

    def get_item_link(self):
        self.random_pause_code(start=1, stop=5)
        for i in range(self.start_page, self.stop_page+1):
            self.send_by_url(url=f'https://999.md/ro/list/phone-and-communication/mobile-phones?page={i}')

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.create_directory(name_directory=self.driver.current_url.split('/')[-1].split('?')[0])
                if self.id_exists('js-ads-container'):
                    container = self.driver.find_element(By.ID, 'js-ads-container').find_elements(By.TAG_NAME, 'a')

                    for link in container:
                        link = link.get_attribute('href')
                        if 'login' not in link:
                            if 'booster' not in link:
                                if 'recommendations' not in link:
                                    self.crate_file(
                                        filename=f"{self.driver.current_url.split('/')[-1].split('?')[0]}/{self.driver.current_url.split('/')[-1].split('?')[0]}_Unsorted_link.txt",
                                        mode='a',
                                        data=link
                                    )

            except NoSuchElementException:
                print('element not found')
            finally:
                self.close_driver()
            self.remove_duplicate(
                default=f"{self.driver.current_url.split('/')[-1].split('?')[0]}/{self.driver.current_url.split('/')[-1].split('?')[0]}_Unsorted_link.txt",
                sorted_filename=f"{self.driver.current_url.split('/')[-1].split('?')[0]}/{self.driver.current_url.split('/')[-1].split('?')[0]}_Sorted_link.txt",
            )



    def close_driver(self):
        """Close the WebDriver instance and quits the browser.

        This method closes the current window and terminates the WebDriver session.
        """
        self.driver.close()  # Close the current window
        self.driver.quit()  # Quit the WebDriver session and close all associated windows


def main():
    return MainParser(
        start_page=1,
        stop_page=2
    )


if __name__ == '__main__':
    main()
