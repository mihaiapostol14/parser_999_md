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
    def __init__(self, start_page=0, stop_page=0):
        # Initialize Firefox options
        self.options = webdriver.FirefoxOptions()

        self.options.set_preference(
            "general.useragent.override",
            USER_AGENT
        )
        self.options.set_preference("dom.webdriver.enabled", False)
        self.options.set_preference("intl.accept_languages", "en-us")
        self.options.set_preference("dom.webnotifications.enabled", False)

        self.service = Service(
            executable_path='GeckoDriver/geckodriver.exe'
        )

        self.driver = webdriver.Firefox(
            service=self.service,
            options=self.options
        )

        self.start_page = start_page
        self.stop_page = stop_page

        self.checker = ElementChecker(driver=self.driver)
        self.driver_helper = DriverHelper(driver=self.driver)

        self.get_item_link()

    def get_item_link(self):
        self.random_pause_code(start=1, stop=5)

        container_class = (
            'styles-module-scss-module__F4-vla__list__container'
        )

        excluded_links = (
            'login?',
            'booster',
            'recommendations',
            'favorites',
            'banner240x400'
        )

        for i in range(self.start_page, self.stop_page + 1):
            self.driver_helper.send_by_url(
                url=f'https://999.md/ro/list/transport/cars?page={i}'
            )

            self.random_pause_code(start=1, stop=5)

            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )

            try:
                current_page = self.driver.current_url.split('/')[-1].split('?')[0]

                self.create_directory(
                    name_directory=current_page
                )

                if self.checker.class_exists(class_name=container_class):
                    container = self.driver.find_element(
                        By.CLASS_NAME,
                        container_class
                    ).find_elements(
                        By.TAG_NAME,
                        'a'
                    )

                    for link in container:
                        link = link.get_attribute('href')

                        if link and all(
                            excluded not in link
                            for excluded in excluded_links
                        ):
                            self.crate_file(
                                filename=f"{current_page}/{current_page}_Unsorted_link.txt",
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