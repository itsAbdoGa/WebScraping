import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class ZillowPipeline:
    def open_spider(self,spider):
        self.file = open("house.json","w") 
        self.houses = []
    def process_item(self, item, spider):
        if item:
            self.houses.append(dict(item))

        return item
    def close_spider(self,spider):
        json.dump(self.houses,self.file,indent=4)


class GoogleSheetsPipeline:
    def open_spider(self, spider):
        # Set up credentials and client
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
        client = gspread.authorize(creds)

        # Open the Google Sheet
        self.sheet = client.open("scrape").sheet1

        # Write the headers to the Google Sheet
        self.headers_written = False

    def process_item(self, item, spider):
        if not self.headers_written:
            self._write_headers(item)
            self.headers_written = True

        row = [item.get('price'), item.get('bedrooms'), item.get('bathrooms'), item.get('sqft'), item.get('address'), item.get('link')]
        self.sheet.append_row(row)

        return item

    def close_spider(self, spider):
        pass

    def _write_headers(self, item):
        headers = [field for field in item.fields]
        self.sheet.append_row(headers)