from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import pandas as pd
import json
class CsvPipeline:
    def open_spider(self,spider):
        self.items = []
    def process_item(self, item, spider):
        if not item["name"]:
            DropItem("invalid name")
        else:
            self.items.append(dict(item))
        return item
    def close_spider(self,spider):
        df = pd.DataFrame(self.items)
        df.to_csv("phones.csv")


class JsonPipeline:
    def open_spider(self,spider):
        self.file = open("phones.json","w")
        self.items = []
    def process_item(self, item, spider):
        if not item["name"]:
            DropItem("invalid name")
        else:
            self.items.append(dict(item))
        return item
    def close_spider(self,spider):
        json.dump(self.items,self.file,indent= 4)


