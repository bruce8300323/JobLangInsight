from datetime import datetime
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as Conditions
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from Job import Job
from JobElementParser import JobElementParser
from Repository import Repository


def find_elements(driver: WebDriver, locator: tuple[str, str]) -> list[WebElement]:
    try:
        return WebDriverWait(driver, 10).until(Conditions.visibility_of_all_elements_located(locator))
    except Exception as e:
        print(e)
        return []

'''
從資訊軟體系統類職缺列表建立職缺 URL 列表供 UpdateJob.py 擷取職缺資訊
'''

options = Options()
options.add_argument("--disable-notifications")
driver = webdriver.Edge(options)
repo = Repository("127.0.0.1", "sa", "Aa123456")
repo.cache()

try:
    driver.get("https://www.104.com.tw/jobs/search/?cat=2007000000&jobsource=2018indexpoc&ro=0")
    contentElement: WebElement = WebDriverWait(driver, 10).until(Conditions.visibility_of_element_located((By.ID, "js-job-content")))
    el = driver.find_element(By.XPATH, '//*[@id="js-job-header"]/div[1]/label[1]/select')
    select = Select(el)
    for i in range(0, len(select.options)):
        select.select_by_index(i)
        current_time = datetime.now()
        print(f"{current_time} Parse Index: {i}")
        jobElements = find_elements(driver, (By.XPATH, '//div[@id="js-job-content"]/article'))
        #for i in range(0, len(jobElements)):
        for element in jobElements:
            # parser = JobElementParser(driver, jobElements[i])
            parser = JobElementParser(driver, element)
            if parser.result != None:
                repo.create_job(parser.result)
except Exception as e:
    print(e)
finally:
    driver.quit()

