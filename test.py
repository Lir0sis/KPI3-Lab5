from datetime import time
from unittest import TestCase
import unittest
from selenium import webdriver
import time
from selenium.webdriver.common import by

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select

from webdriver_manager.chrome import ChromeDriverManager


class Tests(TestCase):
    def setUp(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        browser.implicitly_wait(10)

        self._browser = browser

    def test_search(self):
        browser = self._browser
        browser.get('https://gamebanana.com')
    
        search_request = 'Miku'

        search_bar = browser.find_element(by=By.XPATH, 
            value='//form[@id=\'SearchForm\']//input')

        search_bar.send_keys(search_request)
        search_bar.send_keys(Keys.ENTER)

        result = False 
        for element in browser.find_elements(By.CLASS_NAME, value='Identifiers'):
            name = element.find_element(By.TAG_NAME, value= 'span').text
            result = True if search_request in name else False
            if result: break

        assert result

    def test_mods_filters(self):
        browser = self._browser
        browser.get('https://gamebanana.com/mods')

        browser.maximize_window()

        view_count = 5000

        browser.find_element(by=By.CLASS_NAME, value='ShowFiltersButton').click()

        view_field = browser.find_element(by=By.CLASS_NAME, value='FilterControl_views')
        view_field.find_element(by=By.TAG_NAME, value='legend').click()
        select_field = view_field.find_element(by=By.TAG_NAME, value='select')
        select_field.click()

        Select(select_field).select_by_value(str(view_count))

        browser.find_element(by=By.CLASS_NAME, value='Modal').find_element(by=By.TAG_NAME, value='button').click()


        for element in browser.find_elements(By.CLASS_NAME, value='Stats'):
            count = element.find_element(By.CLASS_NAME, value= 'ViewCount')\
                .find_element(By.TAG_NAME, value= 'itemcount').text

            value = 0
            last_char = count[-1].lower()
            if last_char == 'm' or last_char == 'k':
                value = float(count[0:-2])
                value *= 1000 if last_char == 'k' else 1000000
            else:
                value = float(count)

            assert value >= view_count

    def tearDown(self):
        self._browser.close() 

if __name__ == "__main__":
    unittest.main()

