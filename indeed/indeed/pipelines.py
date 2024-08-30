import pandas as pd


class IndeedPipeline:
    def open_spider(self,spider):
        self.jobs = []
    def process_item(self, item, spider):
        self.jobs.append(item)
        return item
    def close_spider(self,spider):
        df = pd.DataFrame(self.jobs)
        df.to_csv("jobs.csv",index=False)
