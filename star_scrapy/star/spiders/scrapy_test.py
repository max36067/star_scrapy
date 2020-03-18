from scrapy import Spider
from scrapy.http import Request
from datetime import datetime
from urllib.parse import unquote
import copy

class HoroscopeSpider(Spider):
    name = 'star'
    start_urls = ['http://astro.click108.com.tw/']
    def __init__(self):
        self.today = str(datetime.today().date())

    def parse(self, response):
        for star in response.css('div.STAR12_BOX li'):
            href = star.css('a::attr(href)').extract_first().split("=")[-1]
            title = star.css('a::text').extract_first()
            item_dict = {'date':self.today, 'title': title}
            yield Request(url = unquote(href), callback = self.star_info,  meta = {'item':item_dict})

    def star_info(self, response):
        item_dict = response.meta['item']
        for rates in response.css('div.TODAY_CONTENT'):
            all_rate = rates.css('span::text').extract()
            all_content = rates.css('p:nth-child(2n-1)::text').extract()
        for i in range(len(all_rate)):
            item_dict.update({all_rate[i]:all_content[i]})
        yield item_dict
