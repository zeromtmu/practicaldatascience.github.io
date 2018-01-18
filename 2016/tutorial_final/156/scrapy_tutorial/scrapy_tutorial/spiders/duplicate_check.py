from scrapy.exceptions import DropItem
from scrapy_tutorial.items  import CmuItem

class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, CmuItem, spider):
        if item['id'] in self.ids_seen:
            print "duplicate"
            raise DropItem("Repeated items found: %s" % item)
        else:
            self.ids_seen.add(item['id'])
            print "noduplicate"
            return item
