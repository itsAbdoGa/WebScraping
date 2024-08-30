import scrapy
import scrapy.resolver
from scrapy_playwright.page import PageMethod
from itemloaders import ItemLoader
from indeed.items import IndeedItem





class JobsSpider(scrapy.Spider):
    name = "jobs"
    allowed_domains = ["indeed.com"]
    start_urls = ["https://indeed.com"]
    query = "backend developer"
    where = "Remote"
    count = 5
    headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
                "Accept-Language": "en-US,en;q=0.9",
            }
    def start_requests(self):
        
        
        yield scrapy.Request(url=self.start_urls[0],meta={
            "playwright" : True,
            "playwright_page_methods" : [
                PageMethod("fill","input[id='text-input-what']",f"{self.query}"),
                PageMethod("fill","input[id='text-input-where']",f"{self.where}"),
                PageMethod("click","button[type='submit']"),
                PageMethod("wait_for_timeout", 2000)
                
            ],
            "playwright_include_page" : True
            
        },headers=self.headers,callback=self.parse)
    async def parse(self, response):
        page = response.meta["playwright_page"]
       
        jobs = await page.query_selector_all("h2[class*='jobTitle']>a")
        for job in jobs:
            await job.click()
            try :
                title = await page.text_content("h2[data-testid='jobsearch-JobInfoHeader-title'] > span")
                self.logger.info(f"Title Found {title} ")
            except:
                title = "None"
            try : 
                company = await page.text_content("div[data-company-name='true'] > span > a")
                self.logger.info(f"Company Found {company} ")
            except:
                company = "None"
            try :
                rating = await page.text_content("div[data-company-name='true'] + div > span")
                self.logger.info(f"Rating Found {rating} ")
            except:
                rating = "None"
            try :
                location = await page.text_content("div[data-testid*='companyLocation']  > div ")
                self.logger.info(f"Location Found {location} ")
            except:
                location = "None"
            try :
                salary = await page.text_content("div[id='salaryInfoAndJobType'] > span:nth-child(1)")
                self.logger.info(f"salary Found {salary} ")
            except:
                salary = "None"
            try :
                type = await page.text_content("div[id='salaryInfoAndJobType'] > span:nth-child(2)")
                self.logger.info(f"type Found {type} ")
            except:
                type = "None"

            if type == "None":
                type = salary
                salary = "None"


            

            l = ItemLoader(item=IndeedItem())
            l.add_value("company",company)
            l.add_value("title",title)
            l.add_value("rating",rating)
            l.add_value("location",location)
            l.add_value("salary",salary)
            l.add_value("type",type)



            yield l.load_item()
        next_page = response.css("a[data-testid='pagination-page-next']::attr(href)").get()
        if next_page:
            self.logger.info("PAGE FOUND .. PROCEEDING")
            next_url =  response.urljoin(next_page)
            yield scrapy.Request(url=next_url,callback=self.parse,meta={
                "playwright" : True,
                "playwright_page_methods" : [
                    PageMethod("wait_for_timeout", 2000)
                    
                ],
                "playwright_include_page" : True},headers=self.headers)
        else:
            self.logger.warning("NO PAGE FOUND")
