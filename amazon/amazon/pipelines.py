import json
import pandas as pd
import sqlite3

class JsonPipeline:
    def open_spider(self, spider):
        self.file = open('gpus.json', 'w')
        self.items = []

    def close_spider(self, spider):
        json.dump(self.items, self.file, indent=4)
        self.file.close()

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item
    

class CsvPipeline:
    def open_spider(self, spider):
        self.items = []

    def close_spider(self, spider):
        df = pd.DataFrame(self.items)
        df.to_csv('gpus.csv', index=False)

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item
class SqlPipeline:
    def __init__(self):
        self.con = sqlite3.connect("gpus.db")
        self.cur = self.con.cursor()
    def open_spider(self,spider):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS GPU
                         (
                         name TEXT PRIMARY KEY,
                         rating TEXT,
                         ratedby INTEGER,
                         price INTEGER
                         ) """)
        self.con.commit()
    def process_item(self,item,spider):
        self.con.execute("INSERT OR IGNORE INTO GPU VALUES (?,?,?,?)",(item["name"],item["rating"],item["ratedby"],item["price"]))
        self.con.commit()
    def close_spider(self,spider):
        self.con.close()