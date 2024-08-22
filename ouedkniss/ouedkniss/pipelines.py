from itemadapter import ItemAdapter
import json
import pandas as pd
class JsonPipeline:
    def open_spider(self,spider):
        self.file = open("items.json","w")
        self.added_cards = []

    def process_item(self, item, spider):
        self.added_cards.append(dict(item))
        return item
    
    def close_spider(self,spider):
        json.dump(self.added_cards,self.file,indent=4)
        self.file.close()

class CSVPipeline:
    def open_spider(self,spider):
        self.added_cards = []

    def process_item(self, item, spider):
        self.added_cards.append(dict(item))
        return item
    def close_spider(self,spider):
        df= pd.DataFrame(self.added_cards)
        df.to_csv("items.csv",index=False)
