import scrapy
from scrapy.selector import Selector
from itemloaders.processors import MapCompose,TakeFirst
from w3lib.html import remove_tags
def extract_rating(item):
    rating = item.split(" ")[1]
    return rating
def remove_symbol(item):
    num = item.replace('£',"")
    return num
class Booksitem(scrapy.Item):
    name = scrapy.Field(input_processor=MapCompose(remove_tags,str.strip),
        output_processor=TakeFirst())
    rating = scrapy.Field(input_processor=MapCompose(extract_rating,remove_tags,str.strip),
        output_processor=TakeFirst())
    availability = scrapy.Field(input_processor=MapCompose(remove_tags,str.strip),
        output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(remove_symbol,remove_tags,str.strip),
        output_processor=TakeFirst())
    