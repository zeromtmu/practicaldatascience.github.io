# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
from scrapy.exceptions import DropItem


class AddPipeline(object):
    def process_item(self, item, spider):
        vat_factor = "CMU_program: " # the factor we need to add before each program title
        if item['program_title']:
            if item['program_link']:
                item['program_title'][0]= vat_factor+ item['program_title'][0]
            return item
        else:
            raise DropItem("Missing project title in %s" % item)

class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open('cmu.jl', 'wb')

    def process_item(self,item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['program_title'][0] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item['program_title'])
        else:
            self.ids_seen.add(item['program_title'][0])
            return item
