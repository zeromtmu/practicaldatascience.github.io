import scrapy

class YelpSpider(scrapy.Spider):
    name = "yelpspider"
    
    start_urls = [
        'https://www.yelp.com/search?find_desc=Restaurants&find_loc=Pittsburgh,+PA&start=0',
    ]

    def parse(self, response):
        for r in response.css('ul.ylist.ylist-bordered.search-results'):
            yield {
                'restaurant_name': r.css('span.indexed-biz-name a.biz-name.js-analytics-click span::text').extract(),
                'review': [float(x.split(' ')[0]) for x in r.css('div.rating-large i.star-img::attr(title)').extract()],
                'review_counts': [int(x.strip().split(' ')[0]) for x in r.css('span.review-count::text').extract()],
            }
        next_page = response.css('a.u-decoration-none.next.pagination-links_anchor::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)