# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class ArxivPipeline:
    def __init__(self) -> None:
        self.f = open("/home/sharma/Desktop/DeepLearning/Scraper/arxiv/arxiv_python.json", "w")
    def process_item(self, item, spider):
        content = json.dumps(dict(item))+"\n"
        self.f.write(content)
        return item
    def close_spider(self, spider):
        self.f.close()

import pymysql
# reload settngs
from scrapy.utils.project import get_project_settings
class ArxivMySQLPipeline:
    def __init__(self):
        settings = get_project_settings()
        self.host = settings['DB_HOST']
        self.port = settings['DB_PORT']
        self.user = settings['DB_USER']
        # self.name = settings['DB_NAME']
        self.passwd = settings['DB_PASSWD']

        self.connect()

    def connect(self):
        self.conn = pymysql.connect(
            host = self.host,
            port = self.port,
            user = self.user,
            passwd = self.passwd,
        )
        self.cursor = self.conn.cursor()
    
    def process_item(self, item, spider):
        self.cursor.execute('CREATE DATABASE IF NOT EXISTS Arxiv;')
        self.cursor.execute('USE Arxiv;')
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS physicsPaper(id INT AUTO_INCREMENT NOT NULL,\
            title varchar(1024) NOT NULL, authors varchar(4096) NOT NULL, abstraction text,\
            pdflink varchar(256), PRIMARY KEY (id));')
        self.cursor.execute('INSERT INTO physicsPaper(title, authors, abstraction, pdflink) \
                            VALUES("{}","{}","{}","{}")'.format(item['title'], \
                                item['authors'], item['abstraction'], item['download']))
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

    

import urllib.request

class ArxivDownloadPipeline:
    def process_item(self, item, spider):
        url = item.get('download')
        filename = "./papers/" + item.get('title') + ".pdf"
        urllib.request.urlretrieve(url=url, filename=filename)
        return item