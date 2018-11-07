# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import LiepinItem

class LiepinSpider(CrawlSpider):
    name = 'liepin'
    allowed_domains = ['liepin.com']
    start_urls = ['https://www.liepin.com/zhaopin/']

    rules = (
        Rule(LinkExtractor(allow=r'https://www.liepin.com/job/\d+.*'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = LiepinItem()
        item['title'] = response.xpath('//div[@class="title-info"]/h1/text()').extract_first()
        item['price'] = response.xpath('//div[@class="job-title-left"]/p[@class="job-item-title"]//text()').extract_first()
        item['site'] = response.xpath('//p[@class="basic-infor"]/span/a/text()').extract_first()
        item['experience'] = response.xpath('//div[@class="job-qualifications"]/span[2]/text()').extract_first()
        item['education'] = response.xpath('//div[@class="job-qualifications"]/span[1]/text()').extract_first()
        item['time'] = response.xpath('//p[@class="basic-infor"]/time/@title').extract_first()
        description = response.xpath('//div[@class="content content-word"]/text()').extract()
        item['description'] = ''.join(description).strip()
        item['website'] = '猎聘网'
        yield item