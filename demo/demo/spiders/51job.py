# -*- coding: utf-8 -*-
import scrapy
import re
from w3lib.html import remove_tags
from ..items import LiepinItem

class A51jobSpider(scrapy.Spider):
    name = '51job'
    allowed_domains = ['51job.com']
    # start_urls = ['https://search.51job.com/list/000000,000000,0000,00,9,99,%2B,2,1.html']

    def start_requests(self):
        base_url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,%2B,2,{}.html'
        for i in range(1,2001):
            url = base_url.format(str(i))
            req = scrapy.Request(url=url,callback=self.parse)
            yield req


    def parse(self, response):
        html = response.text
        res = re.compile(r'https://jobs.51job.com/.*/\d+.html\?s=01&t=0')
        url_list = re.findall(res, html)
        for url in url_list:
            req = scrapy.Request(url=url,callback=self.parse_info)
            yield req

    def parse_info(self,response):
        html = response.text
        item = LiepinItem()
        title_res = re.compile(r'<h1 title="(.*)">')
        item['title'] = re.findall(title_res, html)[0]
        price_res = re.compile(r'<strong>(.*)</strong>\r\n.*<p class="cname">')
        item['price'] = re.findall(price_res,html)[0]

        data_res = re.compile(r'<p.class="msg.ltype".title="(.*)">')
        data = re.findall(data_res,html)[0]
        res = data.replace('&nbsp;&nbsp;', '')
        data_list = res.split('|')

        if len(data_list) == 4:
            item['site'] = data_list[0]
            if '无' in data_list[1]:
                item['experience'] = '无工作经验'
            else:
                item['experience'] = data_list[1]
            if '招' in data_list[2]:
                item['education'] = '无'
            else:
                item['education'] = data_list[2]
            item['time'] = data_list[3]
        else:
            item['site'] = data_list[0]
            item['experience'] = data_list[1]
            if '招' in data_list[2]:
                item['education'] = '无'
                item['time'] = data_list[3]
            else:
                item['education'] = data_list[2]
                item['time'] = data_list[4]


        description_res = re.compile(r'<div class="bmsg job_msg inbox">(.*)<div class="mt10">',re.S)
        description = re.findall(description_res, html)[0]
        item['description'] = remove_tags(description).strip()
        item['website'] = '51job'
        print(item['title'])
        print(item['price'])
        print(item['site'])
        print(item['experience'])
        print(item['education'])
        print(item['time'])
        print(item['description'])
        yield item

