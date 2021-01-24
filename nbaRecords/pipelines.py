# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import pymongo
import sqlite3

class MongodbPipeline:
    collection_name= "nba_records"

 
    def open_spider(self, spider):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.db = self.client["NBA_RECORDS"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item)
        return item

class SQLlitePipeline:
 
    def open_spider(self, spider):
        self.connection = sqlite3.connect('nbaRecords.db')
        self.c = self.connection.cursor()
        self.c.execute('''
                CREATE TABLE IF NOT EXISTS nba_records(
                    position TEXT,
                    name TEXT,
                    conference TEXT,
                    wins TEXT,
                    losses TEXT
                    )''')

        self.connection.commit()
    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.c.execute('''
                INSERT INTO nba_records (position, name, conference, wins, losses) VALUES(?,?,?,?,?)
                ''', (
                    item.get('position'),
                    item.get('name'),
                    item.get('conference'),
                    item.get('wins'),
                    item.get('losses')
                ))
        self.connection.commit()
        return item