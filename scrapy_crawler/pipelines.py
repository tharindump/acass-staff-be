# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonItemExporter
from scrapy.exceptions import DropItem
from managedb import get_db
import datetime

class ScrapyCrawlerPipeline(object):

    def __init__(self):
        database = get_db()
        self.index_store = database.get_collection('index_store')

    def process_item(self, item, spider):

        url_index = {
            'url': item['url'],
            'score': item['score'],
            'added_date': datetime.datetime.utcnow()
        }

        self.index_store.insert_one(url_index)
        return item


class JsonPipeline(object):
    def __init__(self):
        self.file = open('output.json', 'wb')
        self.exporter = JsonItemExporter(self.file,
                                         encoding='utf-8',
                                         ensure_ascii=False)
        self.exporter.start_exporting()
        self.processed_items = set()

    def process_item(self, item, spider):
        print(item)
        self.exporter.export_item(item)
        if item['url'] in self.processed_items:
            raise DropItem("Duplicate Item Found %s"%item)
        else:
            self.processed_items.add(item['url'])
            return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
        print("\n -------------- Crawled URLS ----------------")
        #for url in self.processed_items:
        #    print(url)
        print(len(self.processed_items))

