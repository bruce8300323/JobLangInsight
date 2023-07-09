from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as Conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from Job import Job
from ParserBase import ParserBase
from Repository import Repository


def JobType(type: str) -> int:
    if type == "全職":
        return 1
    if type.find("兼職") != -1:
        return 2
    return 0

# https://www.104.com.tw/job/74919?jobsource=jolist_b_date
class JobParser(ParserBase):
    # URL
    url: str
    # Job Detail
    detail: str
    # Job Category
    category: list[str]
    # skill
    skill: list[str]
    type: int
    experience: str
    education: list[str]
    hasError: bool
    def __init__(self, driver: WebDriver) -> None:
        """
        Constructor, 
        Parse the job information from the web page, including: url, detail, skill, type, category
        """
        try:
            super().__init__(driver)
            self.driver = driver
            self.url = driver.current_url
            element = self.find_element(By.XPATH, '//div/div/p[@class="mb-5 r3 job-description__content text-break"]')
            self.detail = None if element == None else element.text
            jobType = self.__find_job_type()
            self.type = JobType(jobType)
            self.experience = self.__find_requirement("工作經歷")
            education = self.__find_requirement("學歷要求")
            self.education = education.split("、")
            self.category = self.__parseCategory()        
            self.skill = self.__parseSkill()
            self.hasError = False
        except Exception as ex:
            self.hasError = True
            print(ex)
    
    @property
    def result(self) -> Job | None:
        if self.hasError:
            return None
        tmp = dict(self.__dict__)
        del tmp["driver"]
        del tmp["hasError"]
        return Job(**tmp)

    def __find_job_type(self) -> str:
        rows = self.find_elements((By.XPATH, '//div/div/div[@class="job-description-table row"]/div'))
        for row in rows:
            div = row.find_elements(By.TAG_NAME, "div")
            if len(div) > 1 and div[0].text.strip() == "工作性質":
                return div[1].text.strip()
        return None

    def __parseCategory(self) -> list[str]:
        xpath = '//div/div/div/div[@class="category-item col p-0 job-description-table__data"]/div/div/div/u'
        elements = self.find_elements((By.XPATH, xpath))
        return [i.text for i in elements]
    
    def __find_requirement(self, name: str) -> str:
        rows = self.find_elements((By.XPATH, '//div[@class="job-requirement-table row"]/div'))
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'div')
            if cols[0].text.find(name) != -1:
                return cols[1].text.strip()
        return None

    def __parseSkill(self) -> list[str]:        
        div = self.find_element(By.XPATH, '//div[@class="job-requirement-table row"]/div[5]/div[2]/div')
        if div.text == "不拘":
            requirements = [div]
        else:
            requirements = self.find_elements((By.XPATH, '//div[@class="job-requirement-table row"]/div[5]/div[2]/div/span/a/u'))
        return [r.text for r in requirements]
    

if __name__ == "__main__":
    repo = Repository("127.0.0.1", "sa", "Aa123456")
    repo.cache()
    options = Options()
    options.add_argument("--disable-notifications")
    driver = webdriver.Edge(options)
    try:
        driver.get("https://www.104.com.tw/job/81066")
        parser = JobParser(driver)
        job = parser.result
        if job != None:
            repo.update_job(job)
    except Exception as e:
        print(e)
    finally:
        driver.quit()
        repo.close()