from urllib.parse import urlparse, parse_qs


class Job:
    title: str
    url: str
    industry: str
    company: str
    detail: str
    area: str
    # full time: 1, part time: 2
    type: int
    experience: str
    education: list[str]
    processed: bool
    skill: list[str]
    category: list[str]

    def __init__(self, industry: str = None, company: str = "", title: str = "", area: str = "", type: int = None, url: str = "", detail: str = "", skill: list[str] = None, category: list[str] = None, education: list[str] = [], experience: str = "", processed = None):
        self.industry = industry
        self.company = company
        self.title = title
        self.url = url
        self.detail = detail
        self.area = area
        self.type = type
        self.education = education
        self.experience = experience
        self.skill = [] if skill == None else skill
        self.category = [] if category == None else category
        self.processed = bool(processed)

    @property
    def id(self) -> str:
        if self.url == "" or self.url == None:
            return ""

        parsed_uri = urlparse(self.url)
        jobId = parsed_uri.path.split("/")[-1]
        return jobId

    def __str__(self) -> str:
        edu = ",".join(self.education)
        return f"{self.id} {self.area} {self.title} {self.experience} {edu}"
