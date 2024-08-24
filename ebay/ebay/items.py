import scrapy
from itemloaders.processors import MapCompose,TakeFirst
from w3lib.html import remove_tags
from scrapy.exceptions import DropItem
import re

def format_price(price):
    price = re.sub(r'\$', '', price)
    return price
def format_location(item):
    return re.sub(r'\bfrom\b', '', item)
def format_sold(item):
    result = re.sub(r'\s*\+?\s*sold\s*', '',item)  # Remove 'sold' and optional '+'
    result = re.sub(r',', '', result)  # Remove commas
    return result


class EbayItem(scrapy.Item):
    name = scrapy.Field(input_processor=MapCompose(remove_tags,str.strip),
                        output_processor=TakeFirst())
    status = scrapy.Field(input_processor=MapCompose(remove_tags,str.strip),
                        output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(format_price,remove_tags,str.strip,float),
                        output_processor=TakeFirst())
    location = scrapy.Field(input_processor=MapCompose(format_location,remove_tags,str.strip),
                        output_processor=TakeFirst())
    sold = scrapy.Field(input_processor=MapCompose(format_sold,remove_tags,str.strip,int),
                        output_processor=TakeFirst())
    link = scrapy.Field(input_processor=MapCompose(remove_tags,str.strip),
                        output_processor=TakeFirst())
    pass
