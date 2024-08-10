from typing import Iterable
import scrapy
from itemloaders import ItemLoader
from amazon.items import GPUItem
from urllib.parse import urljoin
class GpusSpider(scrapy.Spider):
    name = "gpus"
    allowed_domains = ["amazon.com"]
    search_term = "gtx"
    start_urls = ["https://www.amazon.com/s?k={search_term}"]
    page_num = 1
    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0].format(search_term=self.search_term),meta= {
            "playwright" : True
        })

    def parse(self, response):
        for gpu in response.css("div[data-component-type='s-search-result']"):
            l = ItemLoader(item=GPUItem(),selector=gpu)
            l.add_css("name","div[data-cy='title-recipe'] h2 a span::text")
            l.add_css("rating","i[data-cy='reviews-ratings-slot'] span::text")
            l.add_css("ratedby","span[aria-label*='ratings']::attr(aria-label)")
            l.add_css("price","span[class='a-price'] span[class='a-price-whole']::text")
            yield l.load_item()
        self.page_num += 1
        
        next_page = response.css(f"a[aria-label='Go to page {self.page_num}']::attr(href)").get()
        if next_page:
            new_url = urljoin(self.start_urls[0].format(search_term=self.search_term),next_page)
            yield scrapy.Request(url=new_url,meta={
                "playwright": True
            })
        
