import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags
import re
def modify_type(item):
    return item.replace("-","")

def clean_title(title):
    if title != "None":
        return re.sub(r"\s-\sjob post$", "", title)
    else:
        return title
class IndeedItem(scrapy.Item):
    title = scrapy.Field(input_processor=MapCompose(clean_title,remove_tags,str.strip),
                         output_processor=TakeFirst())
    company = scrapy.Field(input_processor=MapCompose(remove_tags,str.strip),
                         output_processor=TakeFirst())
    rating = scrapy.Field(input_processor=MapCompose(remove_tags,str.strip),
                         output_processor=TakeFirst())
    location = scrapy.Field(input_processor=MapCompose(remove_tags,str.strip),
                         output_processor=TakeFirst())
    salary = scrapy.Field(input_processor=MapCompose(remove_tags,str.strip),
                         output_processor=TakeFirst())
    type = scrapy.Field(input_processor=MapCompose(modify_type,remove_tags,str.strip),
                         output_processor=TakeFirst())
    
    pass
