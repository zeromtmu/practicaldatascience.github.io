import scrapy

class SimplifiedSimpleSpider(scrapy.Spider):
    name = "simplifiedsimplespider" # name must be unique within project.
    
    # remove start_requests(), use start_urls instead
    start_urls = [
        'https://blog.google/topics/',
    ]
            
    def parse(self, response):
        category = response.url.split('/')[-2]
        file_name = 'Google-simplified-%s.html' % category
        with open(file_name, 'wb') as f:
            f.write(response.body)
        self.log('%s is saved.' % file_name)