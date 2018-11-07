# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import LiepinItem

class ZhilianSpider(scrapy.Spider):
    name = 'zhilian'
    allowed_domains = ['zhaopin.com']
    # start_urls = ['http://zhaopin.com/']

    def start_requests(self):
        for v in range(530,600):
            base_url = 'https://fe-api.zhaopin.com/c/i/sou?start={}&pageSize=60&cityId='+str(v)+'&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kt=3&lastUrlQuery=%7B%22p%22:2,%22pageSize%22:%2260%22,%22jl%22:%22530%22,%22kt%22:%223%22%7D'
            for i in range(1,300):
                page = 60 * i
                url = base_url.format(page)
                req = scrapy.Request(url=url,callback=self.parse)
                yield req

    def parse(self, response):
        data_dict = json.loads(response.body.decode('utf-8'))
        data_list = data_dict['data']['results']
        for url in data_list:
            url_info = url['positionURL']
            req = scrapy.Request(url=url_info,callback=self.parse_info)
            yield req

    def parse_info(self,response):
        item = LiepinItem()
        if response.xpath('//h1/text()').extract_first():
            if response.xpath('//ul[@class="terminal-ul clearfix"]/li[1]/strong/text()').extract_first():
                item['title'] = response.xpath('//h1/text()').extract_first()
                item['price'] = response.xpath('//ul[@class="terminal-ul clearfix"]/li[1]/strong/text()').extract_first()
                site = response.xpath('//ul[@class="terminal-ul clearfix"]/li[2]/strong//text()').extract()
                item['site'] = ''.join(site)
                item['experience'] = response.xpath('//ul[@class="terminal-ul clearfix"]/li[5]/strong/text()').extract_first()
                item['education'] = response.xpath('//ul[@class="terminal-ul clearfix"]/li[6]/strong/text()').extract_first()
                item['time'] = response.xpath('//ul[@class="terminal-ul clearfix"]/li[3]/strong/span/text()').extract_first()
                description = response.xpath('//div[@class="tab-inner-cont"]/p/text()').extract()
                item['description'] = ''.join(description).strip()
                item['website'] = '智联招聘'
                yield item
            else:
                print('无数据')
