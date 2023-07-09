from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as Conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from Job import Job

class JobElementParser:

    def __init__(self, driver: WebDriver, element: WebElement) -> None:
        """
        Constructor, 
        Parse the job information from the element, including: company, industry, title, area, url
        """
        try:
            path = '//div[@id"js-job-content"]/article'
            # WebDriverWait(driver, 10).until(Conditions.presence_of_element_located(By.XPATH, ))
            # self.driver = driver
            self.company = element.get_attribute("data-cust-name")
            self.industry = element.get_attribute("data-indcat-desc")
            anchor = element.find_element(By.XPATH, "div[1]/h2/a")
            self.title = anchor.text            
            self.area = element.find_element(By.XPATH, "div/ul[2]/li[1]").text
            self.url = anchor.get_attribute("href")
        except Exception as e:
            print(e)

    @property
    def result(self) -> Job | None:
        """
        Return Job from the parsing result if url exists, otherwise return None
        """
        if "url" not in self.__dict__:
            return None
        return Job(**self.__dict__)