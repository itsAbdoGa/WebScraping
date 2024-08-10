from itemloaders.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags
import scrapy
import re


# x out y stars --> x/y
def modify_rating(text):

    return re.sub(r"(\d+\.\d+) out of (\d+) stars", r"\1/\2", text)

# x ratings --> x
def modify_ratedby(text):
    
    return re.sub(r"(\d{1,3}(?:,\d{3})*) ratings", lambda m: m.group(1).replace(',', ''), text)


class GPUItem(scrapy.Item):
    name = scrapy.Field(input_processor=MapCompose(remove_tags,str.strip),
                        output_processor=TakeFirst())
    rating = scrapy.Field(input_processor=MapCompose(remove_tags,str.strip,modify_rating),
                        output_processor=TakeFirst())
    ratedby = scrapy.Field(input_processor=MapCompose(remove_tags,str.strip,modify_ratedby,int),
                        output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(remove_tags,str.strip,int),
                        output_processor=TakeFirst())
    
    
    
    pass
