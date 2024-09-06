import scrapy
from itemloaders.processors import MapCompose,TakeFirst
import re

def format_prsqft(num):
    n = ''.join(re.findall(r"\d+", num)) 
    if n:
        return int(n)
    else:
        return "N/A"

def format_bdba(num):
    if num.isdigit():
        return int(num)
    else:
        return num

class ZillowItem(scrapy.Item):
    price = scrapy.Field(input_processor=MapCompose(str.strip,format_prsqft),
                         output_processor=TakeFirst())
    bedrooms = scrapy.Field(input_processor=MapCompose(str.strip,format_bdba),
                         output_processor=TakeFirst())
    bathrooms = scrapy.Field(input_processor=MapCompose(str.strip,format_bdba),
                         output_processor=TakeFirst())
    sqft = scrapy.Field(input_processor=MapCompose(str.strip,format_prsqft),
                         output_processor=TakeFirst())
    address = scrapy.Field(input_processor=MapCompose(str.strip),
                         output_processor=TakeFirst())
    link = scrapy.Field(input_processor=MapCompose(str.strip),
                         output_processor=TakeFirst())

    pass
