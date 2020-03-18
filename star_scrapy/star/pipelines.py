# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

class StarPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoDBPipeline:
    print('Pipeline')
    def open_spider(self, spider):
        db_uri = spider.settings.get('MONGODB_URI')
        db_name = spider.settings.get('MONGODB_DB_NAME')
        self.db_coll = spider.settings.get('MONGODB_DB_COL')
        self.db_client = pymongo.MongoClient(db_uri)
        self.coll = self.db_client[db_name][self.db_coll]

    def process_item(self, item, spider):
        self.insert_article(item)
        return item

    def insert_article(self, item):
        item = dict(item)
        self.coll.insert_one(item)
        print('資料插入完成')

    def close_spider(self, spider):
        self.db_client.close()