import scrapy
from itemloaders import ItemLoader
from books.items import Booksitem
from scrapy_playwright.page import PageMethod 
class BookscrapeSpider(scrapy.Spider):
    name = "bookscrape"
    allowed_domains = ["books.toscrape.com"]
    start_page = 1
    base_url = "https://books.toscrape.com/catalogue/page-{page}.html"



    def start_requests(self):
        url = self.base_url.format(page=self.start_page)
        yield scrapy.Request(url,meta=dict(
            playwright = True,
            playwright_page_methods = [
                    PageMethod('wait_for_selector', 'article.product_pod')  # Ensure content is loaded
                ]
        )

        )
    def parse(self, response):
            for book in response.css("article.product_pod"):
                l = ItemLoader(item=Booksitem(),selector=book)
                l.add_css("name","h3 > a::attr(title)")
                l.add_xpath("rating",".//p[contains(@class,'star-rating')]/@class")
                l.add_css("availability","p[class='instock availability']::text")
                l.add_css("price","p[class='price_color']::text")
                yield l.load_item()
            next_page = response.css('li.next a::attr(href)').get()
            if next_page:
                next_page_url = response.urljoin(next_page)  # Build absolute URL for the next page
                yield scrapy.Request(
                    next_page_url,
                    meta=dict(playwright=True, playwright_page_methods=[
                         PageMethod("wait_for_selector","article.product_pod")
                    ])
                )
        


