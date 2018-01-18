# change the cmuspider.py file again to store item field by the following code:
import scrapy

from scrapy_tutorial.items import CmuItem  # don't forget to import CmuItem we defined before

class CmuSpider(scrapy.Spider):
    name = "cmu"
    allowed_domains = ["cmu.edu"]
    start_urls = [ "http://www.cmu.edu/academics/interdisciplinary-programs.html"]

    def parse(self, response):
        for sel in response.xpath('//div[@class=""]/ul/li'):
            item = CmuItem()
            item['program_title'] = sel.xpath('a/text()').extract()
            item['program_link'] = sel.xpath('a/@href').extract()
            print "program_title", item['program_title']
            print "program_link",item['program_link']
            yield item
