# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re
from jobparser.items import JobparserItem


class JobparserPipeline:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.mongo_base = self.client.task5

    def process_item(self, item, spider):
        if not isinstance(item, JobparserItem):
            return item

        collection = self.mongo_base[spider.name]
        print(item['name'])
        try:
            min_ = item['salary_min'][0]
        except IndexError:
            min_ = 0
        try:
            max_ = item['salary_max'][0]
        except IndexError:
            max_ = 0
        item['salary'] = {'min': min_, 'max': max_}

        try:
            item['url'] = item['url'][0]
        except IndexError:
            None
        del item['salary_max']
        del item['salary_min']
        collection.insert_one(item)
        return item


class JobparserPipelineSJ(object):
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.mongo_base = self.client.task5

    def process_item(self, item, spider):
        if not isinstance(item, JobparserItemSJ):
            return item

        collection = self.mongo_base[spider.name]
        print(item['name'])
        try:
            min_ = int(''.join(re.findall(r'\d', item['salary'][0])))
        except IndexError:
            min_ = 0
        try:
            max_ = int(''.join(re.findall(r'\d', item['salary'][4])))
        except IndexError:
            max_ = 0
        item['salary'] = {'min': min_, 'max': max_}
        collection.insert_one(item)
        return item