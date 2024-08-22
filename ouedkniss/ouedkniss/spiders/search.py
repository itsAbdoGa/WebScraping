import scrapy
from scrapy_playwright.page import PageMethod
from itemloaders import ItemLoader
from ouedkniss.items import OuedknissItem

class SearchSpider(scrapy.Spider):
    name = "search"
    allowed_domains = ["ouedkniss.com"]
    url = "https://www.ouedkniss.com/s/{page}?keywords={query}"
    start_page = 1
    query = "iphone"
    pagenum = 5
    def start_requests(self):
        yield scrapy.Request(url=self.url.format(page=self.start_page,query=self.query),meta={
            "playwright": True,
           "playwright_page_methods": [
                    PageMethod("wait_for_timeout", 2000), 
                    PageMethod("evaluate", """
                        let totalHeight = 0;
                        let distance = 300;
                        function sleep(ms) {
                            return new Promise(resolve => setTimeout(resolve, ms));
                        }
                        async function scroll() {
                            while (totalHeight < document.body.scrollHeight) {
                                window.scrollBy(0, distance);
                                totalHeight += distance;
                                await sleep(200);  // Wait 1000ms between scrolls
                            }
                        }
                        scroll();
                    """)]
        })



    def parse(self, response):
            for card in response.css("div[class*='o-announ-card-full']"):
                l = ItemLoader(item=OuedknissItem(),selector=card)
                l.add_css("name" ,"h3[class*='o-announ-card-title']::text")
                l.add_css("price" ,"span.price div[dir='ltr']::text")
                l.add_css("payment_on_delivery","h3[class*='o-announ-card-title'] ~ span")
                l.add_css("link","div > a[class*='o-announ-card-content']::attr(href)")
                l.add_css("location", "div[class='mb-1 d-flex flex-column flex-gap-1 line-height-1']>span:nth-child(1)::text")
                l.add_css("time","div[class='mb-1 d-flex flex-column flex-gap-1 line-height-1']>span:nth-child(2)::text")
                l.add_css("seller","div>div:nth-child(2)>a>div::text")
                yield l.load_item()
                self.start_page += 1
                if self.start_page < self.pagenum:
                    next_page = self.url.format(page=self.start_page, query=self.query)
                    yield scrapy.Request(
                        url=next_page,
                        meta={
                            "playwright": True,
                            "playwright_page_methods": [
                                PageMethod("wait_for_timeout", 2000),
                                PageMethod(
                                    "evaluate",
                                    """
                                    let totalHeight = 0;
                                    let distance = 300;
                                    async function sleep(ms) {
                                        return new Promise(resolve => setTimeout(resolve, ms));
                                    }
                                    async function scroll() {
                                        while (totalHeight < document.body.scrollHeight) {
                                            window.scrollBy(0, distance);
                                            totalHeight += distance;
                                            await sleep(200);
                                        }
                                    }
                                    await scroll();
                                    """,
                                ),
                            ],
                        },
                        callback=self.parse,
                    )