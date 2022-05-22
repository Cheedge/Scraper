# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class ArxivPipeline:
    def __init__(self) -> None:
        self.f = open("/home/sharma/Desktop/DeepLearning/Scraper/arxiv/Arxiv_python.json", "w")
    def process_item(self, item, spider):
        content = json.dumps(dict(item))+"\n"
        self.f.write(content)
        return item
