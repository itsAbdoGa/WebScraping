import scrapy
from itemloaders.processors import MapCompose,TakeFirst
from w3lib.html import remove_tags
#remove spaces from str
def modify_price(item):
    return item.replace(" ","")

def delivery_check(item):
    if item == "[]":
        return False
    else:
        return True

def get_link(item):
    url = "https://ouedkniss.com"
    return url+item

class OuedknissItem(scrapy.Item):
    name = scrapy.Field(input_processor=MapCompose(remove_tags,str.strip),
                        output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(modify_price,remove_tags,str.strip,float),
                        output_processor=TakeFirst())
    payment_on_delivery = scrapy.Field(input_processor=MapCompose(remove_tags,delivery_check),
                           output_processor=TakeFirst())
    link = scrapy.Field(input_processor=MapCompose(remove_tags,get_link,str.strip),
                        output_processor=TakeFirst())
    location = scrapy.Field(input_processor=MapCompose(remove_tags,str.strip),
                        output_processor=TakeFirst())
    time = scrapy.Field(input_processor=MapCompose(remove_tags,str.strip),
                        output_processor=TakeFirst())
    seller = scrapy.Field(input_processor=MapCompose(remove_tags,str.strip),
                        output_processor=TakeFirst())
