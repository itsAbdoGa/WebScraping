import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.selector import Selector
from itemloaders import ItemLoader
from zillow.items import ZillowItem


class HouseSpider(scrapy.Spider):
    name = "house"
    allowed_domains = ["zillow.com"]
    start_urls = ["https://zillow.com/ny"]
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'Cookie': 'search=6|1727977054466%7C%09%0943%09%7B%22isList%22%3Atrue%7D%09%09%09%09%09; zgsession=1|ce598d1a-576d-4f91-bbbd-f0d4bb2e556c; zguid=24|%242e4bda4a-8f40-40d0-9fb8-fbdeecd418e3; AWSALB=ZLLmRR6w+1BTTqyl+0sLZgm6X/bRKWsPBMvRZ1FhKlMYlw6qYd6ckaCm/3CGSHFw9cXxM3rZa85YJ8ID0IiBYU26HC9Sk8Ef0c0JpeykSqQryr3cC0PTHY8xUxEE; AWSALBCORS=ZLLmRR6w+1BTTqyl+0sLZgm6X/bRKWsPBMvRZ1FhKlMYlw6qYd6ckaCm/3CGSHFw9cXxM3rZa85YJ8ID0IiBYU26HC9Sk8Ef0c0JpeykSqQryr3cC0PTHY8xUxEE; JSESSIONID=ED5213D433D4F3487FBFF9AA6CD250A8'
    }
    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0],meta={
            "playwright" : True,
            "playwright_page_methods" : [
                PageMethod("wait_for_timeout",2000),
                
                                         ],
            "playwright_include_page" : True
        },headers=self.headers,callback=self.scroll)

   
    async def scroll(self, response):
        page = response.meta["playwright_page"]
        scroll = 6
        i = 0 
        
        
        await page.hover("div[id='grid-search-results']>ul>li:nth-child(1)")
        
        # Scroll multiple times
        while i < scroll:
            await page.mouse.wheel(0, 1000)
            i += 1

        await page.wait_for_timeout(2000)
        content = await page.content()

        await page.close()

        
        return self.parse_page_content(content)

    def parse_page_content(self, content):

        response = Selector(text=content)
        
        for house in response.css("div[id='grid-search-results']>ul>li[class*='ListItem']"):
            l = ItemLoader(item=ZillowItem(),selector=house)
            l.add_css("price","span[data-test='property-card-price']::text")
            l.add_css("bedrooms","ul[class*='StyledPropertyCardHomeDetailsList'] > li:nth-child(1) > b::text")
            l.add_css("bathrooms","ul[class*='StyledPropertyCardHomeDetailsList'] > li:nth-child(2) > b::text")
            l.add_css("sqft","ul[class*='StyledPropertyCardHomeDetailsList'] > li:nth-child(3) > b::text")
            l.add_css("address","address[data-test='property-card-addr']::text")
            l.add_css("link","a[data-test='property-card-link']::attr(href)")


            yield l.load_item()
        