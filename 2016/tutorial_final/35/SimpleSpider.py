import scrapy

class SimpleSpider(scrapy.Spider):
    name = "simplespider" # name must be unique within project.
    
    def start_requests(self):
        urls = [
            'https://blog.google/products/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
    def parse(self, response):
        category = response.url.split('/')[-2]
        file_name = 'Google-%s.html' % category
        with open(file_name, 'wb') as f:
            f.write(response.body) # simply record all the contents of page
        self.log('%s is saved.' % file_name)