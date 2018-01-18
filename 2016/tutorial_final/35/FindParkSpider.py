import scrapy

class FindParkSpider(scrapy.Spider):
    name = "findparkspider"
    
    states = ['ca']
    start_urls = [
        'https://www.nps.gov/state/ak/index.htm',
        'https://www.nps.gov/state/ca/index.htm',
    ]

    def parse(self, response):
        for r in response.css('div#parkListResultsArea'):
            yield {
                'park_name': r.css('h3 a::text').extract(),
                'park_description': r.css('div.list_left p::text').extract(),
            }