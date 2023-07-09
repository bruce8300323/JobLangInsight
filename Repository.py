import pyodbc
from pyodbc import Connection

from Category import Category
from Company import Company
from Education import Education
from Job import Job
from Skill import Skill
import Text

class Repository:
    closed: bool
    conn: Connection
    companies: dict[any, Company]
    educations: dict[any, Education]
    skills: dict[any, Skill]
    categories: dict[any, Skill]

    def __init__(self, server: str, user: str, password: str, dbName: str = "JobLangInsight") -> None:
        self.conn = pyodbc.connect(
            "Driver={SQL Server};"
            f"Server={server};"
            f"Database={dbName};"
            f"UID={user};"
            f"PWD={password};"
        )
        self.closed = False
        self.companies = dict()
        self.categories = dict()
        self.educations = dict()
        self.skills = dict()

    def __del__(self):
        self.close()

    def close(self):
        if not self.closed:
            self.conn.close()
            self.closed = True

    def cache(self):
        skills = self.get_skills()
        for skill in skills:
            self.skills[skill.name] = skill

        categories = self.get_categories()
        for category in categories:
            self.categories[category.name] = category

        educations = self.get_educations()
        for education in educations:
            self.educations[education.degree] = education

    def create_company(self, name: str, category: str = "", commit: bool = True):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO Company (Name, Category) VALUES (?, ?)", name, category)
        if commit:
            self.conn.commit()
        cursor.close()

    def update_company(self, company: Company):
        cursor = self.conn.cursor()
        cursor.execute("update company set name = ?, category = ? where id = ?",
                       company.name, company.category, company.id)
        self.conn.commit()
        cursor.close()

    def get_company_id(self, name: str, category: str = "") -> str | None:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM Company where name = ?", name)
        row = cursor.fetchone()
        if row == None:
            self.create_company(name, category)
            cursor.execute("SELECT id FROM Company where name = ?", name)
            row = cursor.fetchone()

        if row == None:
            cursor.close()
            return None

        id = row.id
        cursor.close()
        return id

    def create_education(self, degree: str) -> Education:
        cursor = self.conn.cursor()
        cursor.execute("insert into education(degree) values(?)", degree)
        cursor.execute("SELECT @@Identity")
        id = cursor.fetchval()
        self.conn.commit()
        cursor.close()
        return Education(id, degree)
    
    def get_education(self, name: str) -> Education | None:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, degree FROM Education where degree = ?", name)
        row = cursor.fetchone()
        education = None if row == None else Education(*row)
        cursor.close()
        return education

    def get_educations(self) -> list[Education]:
        cursor = self.conn.cursor()
        cursor.execute("select id, degree from education")
        rows = cursor.fetchall()
        return [Education(*row) for row in rows]

    def get_categories(self) -> list[Category]:
        categories: list[Category] = []
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name FROM Category")
        rows = cursor.fetchall()
        for row in rows:
            category = Category(row.id, row.name)
            categories.append(category)
        return categories

    def create_skill(self, name: str, alias: str = "") -> Skill:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO SKILL (Name, Alias) VALUES(?, ?)", name, alias)
        cursor.execute("SELECT @@Identity")
        id = cursor.fetchval()
        self.conn.commit()
        cursor.close()
        return Skill(id, name, set(alias.split(",")))

    def get_skill(self, name: str) -> Skill:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, name, alias FROM Skill where name = ?", name)
        row = cursor.fetchone()
        if row == None:
            cursor.close()
            return None

        alias = set() if row.alias == None or row.alias == "" else set(row.alias.split())
        skill = Skill(row.id, row.name, alias)
        cursor.close()
        return skill

    def get_skills(self) -> list[Skill]:
        skills: list[Skill] = []
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, alias FROM Skill")
        rows = cursor.fetchall()
        for row in rows:
            alias: set = set() if row.alias == "" or row.alias == None else set(row.alias.split(","))
            skill = Skill(row.id, row.name, alias)
            skills.append(skill)
        cursor.close()
        return skills

    def create_category(self, name: str) -> Category:
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO CATEGORY (Name) VALUES(?)", name)
        cursor.execute("SELECT @@Identity")
        id = cursor.fetchval()
        self.conn.commit()
        cursor.close()
        return Category(id, name)

    def get_category(self, name: str) -> Category:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name from category where name = ?", name)
        row = cursor.fetchone()
        if row == None:
            cursor.close()
            return None

        cursor.close()
        return Category(row.id, row.name)

    def get_categories(self) -> list[Category]:
        categories: list[Category] = []
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name FROM Category")
        rows = cursor.fetchall()
        for row in rows:
            category = Category(row.id, row.name)
            categories.append(category)
        return categories

    def create_job(self, job: Job):
        if job.id == "" or job.company == '' or job.company == None:
            print(f"Skip Job ({job.company}, {job.title})")
            return

        try:
            cursor = self.conn.cursor()
            # Company-Job Relation
            company = self.get_company_by_name(job.company)
            if company == None:
                companyId = self.get_company_id(job.company, job.industry)
            else:
                companyId = company.id

            cursor.execute(
                "select companyId from CompanyJob where CompanyId = ? and JobId = ?", companyId, job.id)
            exists = cursor.fetchval() != None
            if not exists:
                cursor.execute(
                    "insert into CompanyJob(CompanyId, JobId) values(?, ?)", companyId, job.id)

            # Job-Skill Relation
            if job.skill != None and len(job.skill) > 0:
                for s in job.skill:
                    if s not in self.skills:
                        skill = self.get_skill(s)
                        if skill == None:
                            skill = self.create_skill(s)
                        self.skills[s] = skill
                    skill = self.skills[s]
                    cursor.execute(
                        "insert into JobSkill(JobId, SkillId) values(?, ?)", job.id, skill.id)
            # Job-Category Relation
            if job.category != None and len(job.category) > 0:
                for c in job.category:
                    if c not in self.categories:
                        category = self.get_category(c)
                        if category == None:
                            category = self.create_category(c)
                        self.categories[c] = category
                    category = self.categories[c]
                    cursor.execute(
                        "insert into CategoryJob (CategoryId, JobId) values(?, ?)", category.id, job.id)
            # Job-Education
            for edu in job.education:
                if edu not in self.educations:
                    education = self.get_education(edu)
                    if education == None:
                        education = self.create_education(edu)
                    self.educations[edu] = education
                education = self.educations[edu]
                cursor.execute("insert into JobEducation(JobId, EducationId) values(?, ?)", job.id, education.id)
            # Job
            cursor.execute("insert into Job (id, title, url, area, type, detail, experience, processed) values(?, ?, ?, ?, ?, ?, ?, ?)",
                           job.id, job.title, job.url, job.area, job.type, job.detail, job.experience, job.processed)
            self.conn.commit()
        except Exception as ex:
            print(ex)
        finally:
            cursor.close()

    def get_job(self, jobId: str) -> Job:
        if jobId == "" or jobId == None:
            return None

        cursor = self.conn.cursor()
        cursor.execute('''
        select c.name, c.category, j.id, j.title, j.url, j.area, j.type, j.detail, j.processed 
        from Job as J left join CompanyJob as CJ on j.Id = cj.JobId
        left join Company as C on cj.CompanyId = c.Id
        where j.id = ?''', jobId)
        row = cursor.fetchone()
        if row == None:
            cursor.close()
            return None
        job = Job(row.category, row.name, row.title, row.area,
                  row.type, row.url, row.detail, processed=row.processed)
        cursor.close()
        return job

    def update_job(self, job: Job):
        oldJob = self.get_job(job.id)
        if oldJob == None:
            return

        if Text.isNoneOrEmpty(job.area) and not Text.isNoneOrEmpty(oldJob.area):
            job.area = oldJob.area
        if Text.isNoneOrEmpty(job.experience) and not Text.isNoneOrEmpty(oldJob.experience):
            job.experience = oldJob.experience
        
        try:
            cursor = self.conn.cursor()
            # Company-Job Relation
            if job.company != "" and job.company != None:
                company = self.get_company_by_name(job.company)
                if company == None:
                    companyId = self.get_company_id(job.company, job.industry)
                else:
                    companyId = company.id
                cursor.execute(
                    "delete from CompanyJob where CompanyId = ? and JobId = ?", companyId, job.id)
                cursor.execute(
                    "insert into CompanyJob(CompanyId, JobId) values(?, ?)", companyId, job.id)
            # Job-Skill Relation
            if job.skill != None and len(job.skill) > 0:
                cursor.execute("delete from JobSkill where JobId = ?", job.id)
                for s in job.skill:
                    if s not in self.skills:
                        skill = self.get_skill(s)
                        if skill == None:
                            skill = self.create_skill(s)
                        self.skills[s] = skill
                    skill = self.skills[s]
                    cursor.execute(
                        "insert into JobSkill(JobId, SkillId) values(?, ?)", job.id, skill.id)
            # Job-Category Relation
            if job.category != None and len(job.category) > 0:
                cursor.execute(
                    "delete from CategoryJob where JobId = ?", job.id)
                for c in job.category:
                    if c not in self.categories:
                        category = self.get_category(c)
                        if category == None:
                            category = self.create_category(c)
                        self.categories[c] = category
                    category = self.categories[c]
                    cursor.execute(
                        "insert into CategoryJob (CategoryId, JobId) values(?, ?)", category.id, job.id)
            # Job-Education Relation
            cursor.execute("delete from JobEducation where JobId = ?", job.id)
            for edu in job.education:
                if edu not in self.educations:
                    education = self.get_education(edu)
                    if education == None:
                        education = self.create_education(edu)
                    self.educations[edu] = education
                education = self.educations[edu]
                cursor.execute("insert into JobEducation(JobId, EducationId) values(?, ?)", job.id, education.id)
            # Job
            cursor.execute("update Job set area = ?, type = ?, detail = ?, experience = ?, processed = 1 where id = ?",
                           job.area, job.type, job.detail, job.experience, job.id)
            self.conn.commit()
        except Exception as ex:
            print(ex)
        finally:
            cursor.close()
