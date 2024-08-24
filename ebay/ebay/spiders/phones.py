import scrapy
from scrapy_playwright.page import PageMethod
from itemloaders import ItemLoader
from ebay.items import EbayItem

class PhonesSpider(scrapy.Spider):
    name = "phones"
    allowed_domains = ["ebay.com"]
    start_urls = ["https://www.ebay.com"]
    query = "phones"
    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0],callback=self.parse,
                             meta={
                                 "playwright" : True,
                                 "playwright_page_methods" : [
                                     PageMethod("fill","input[aria-label='Search for anything']",f"{self.query}"),
                                     PageMethod("click","input[type='submit']"),
                                     PageMethod("wait_for_timeout",4000)

                                 ],
                               
                             })
    
    
    def parse(self, response):
        for item in response.css("ul[class*='srp-results']>li[id*=item]"):
            l = ItemLoader(item=EbayItem(),selector=item)
            l.add_css("name","div[class*='s-item__title'] > span::text")
            l.add_css("status","span.SECONDARY_INFO::text")
            l.add_css("price","span.s-item__price::text")
            l.add_css("location","span[class*='s-item__location']::text")
            l.add_css("sold","span[class*='s-item__quantitySold']>span::text")      
            l.add_css("link","a[class='s-item__link']::attr(href)")  
            yield l.load_item()