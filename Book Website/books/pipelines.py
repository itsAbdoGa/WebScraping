import pandas as pd
import sqlite3
import json

class JsonPipeline:
    def open_spider(self, spider):
        # Open the JSON file in write mode using context management
        self.file = open('books.json', 'w')
        # Initialize an empty list to accumulate items
        self.items = []

    def process_item(self, item, spider):
        # Ensure the item is not None and convert it to a dictionary
        if item is not None:
            item_dict = dict(item)
            print(f"Processing item: {item_dict}")
            self.items.append(item_dict)
        else:
            print("Received None item")
        return item

    def close_spider(self, spider):
        # Check if there are items to write
        if self.items:
            # Write all accumulated items to the JSON file
            json.dump(self.items, self.file, indent=4)
        else:
            print("No items to write.")
        self.file.close()

class BooksPipeline:
    def process_item(self, item, spider):
        return item
    
class CsvDatabasePipeline:
    def __init__(self):
        self.elements = []
    def process_item(self,item,spider):
        self.elements.append(item)
        return item
    def close_spider(self,spider):
        df = pd.DataFrame(self.elements)
        df.to_csv("books.csv",index=False)
class SqlDatababsePipeline:
    def __init__(self):
        self.con = sqlite3.connect("books.db")
        self.cur = self.con.cursor()
    def open_spider(self,spider):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS books (
                            name TEXT PRIMARY KEY,
                            rating TEXT,
                            availability TEXT,
                            price INTEGER)
                         """)
        self.con.commit()
    def process_item(self,item,spider):
        self.con.execute("""INSERT OR IGNORE  INTO  books (name,rating,availability,price) VALUES (?,?,?,?)""",
                         (item["name"],item["rating"],item["availability"],item["price"]))
        self.con.commit()
        return item
        
    def close_spider(self,spider):
        self.con.close()
        
        
        
        
