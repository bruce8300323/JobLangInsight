from datetime import datetime
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as Conditions
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from JobParser import JobParser
from JobElementParser import JobElementParser
from Repository import Repository
import JobRepository 


def find_elements(driver: WebDriver, locator: tuple[str, str]) -> list[WebElement]:
    try:
        return WebDriverWait(driver, 10).until(Conditions.visibility_of_all_elements_located(locator))
    except Exception as e:
        print(e)
        return []
    

options = Options()
options.add_argument("--disable-notifications")
driver = webdriver.Edge(options)
jobIds = JobRepository.GetJobsFromDb()
# jobIds = JobRepository.GetJobsFromDir()
repo = Repository("127.0.0.1", "sa", "Aa123456")
# repo = JsonRepository()
repo.cache()

try:
    driver.get("https://www.104.com.tw/jobs/search/?cat=2007000000&jobsource=2018indexpoc&ro=0")
    contentElement: WebElement = WebDriverWait(driver, 10).until(Conditions.visibility_of_element_located((By.ID, "js-job-content")))
    el = driver.find_element(By.XPATH, '//*[@id="js-job-header"]/div[1]/label[1]/select')
    select = Select(el)
    for i in range(0, len(select.options)):
        random_number = random.uniform(1, 15)
        time.sleep(random_number)
        select.select_by_index(i)
        current_time = datetime.now()
        print(f"{current_time} Parse Index: {i}")
        jobElements = find_elements(driver, (By.XPATH, '//div[@id="js-job-content"]/article'))
        #for i in range(0, len(jobElements)):
        for element in jobElements:
            # parser = JobElementParser(driver, jobElements[i])
            parser = JobElementParser(driver, element)
            job = parser.result
            jobDetail = None
            if job != None and job.id not in jobIds:
                driver.execute_script(f"window.open('{job.url}');")
                driver.switch_to.window(driver.window_handles[1])
                detail = JobParser(driver)                
                jobDetail = detail.result
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            if jobDetail == None:
                # TODO: save to wait list
                continue
            else:
                job.detail = jobDetail.detail
                job.skill = jobDetail.skill
                job.category = jobDetail.category
                job.type = jobDetail.type
                job.processed = True
                repo.create_job(job)
                jobIds.add(job.id)
                random_number = random.uniform(1, 5)
                time.sleep(random_number)
except Exception as e:
    print(e)
finally:
    driver.quit()
    repo.close()