from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as Conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class ParserBase:

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def find_element(self, by: str, query: str) -> WebElement:
        return WebDriverWait(self.driver, 10).until(Conditions.visibility_of_element_located((by, query)))

    def find_elements(self, locator: tuple[str, str]) -> list[WebElement]:
        return WebDriverWait(self.driver, 10).until(Conditions.visibility_of_all_elements_located(locator))
