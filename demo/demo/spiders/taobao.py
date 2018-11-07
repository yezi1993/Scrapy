# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import TaobaoItem

class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['taobao.com']
    # start_urls = ['https://s.m.taobao.com/search?&q=%E8%A3%99%E5%AD%90&sst=1&n=20&buying=buyitnow&m=api4h5&abtest=30&wlsort=30&page=2']

    def start_requests(self):
        keyword = ['薄呢外套','毛衣','马甲','皮衣','裙子','厚底鞋','短外套','包臀裙','哈伦裤','套头衫','九分裤','真皮','牛仔裤','长袖t恤','牛仔衬衫','板鞋','内衣','情侣装','网面鞋','商务休闲','风衣','靴子','内裤','护肤套装','家居服','帽子','夹克','手机壳','零食','男表']
        for key in keyword:
            base_url = 'https://s.m.taobao.com/search?&q='+key+'&sst=1&n=20&buying=buyitnow&m=api4h5&abtest=30&wlsort=30&page={}'
            for i in range(1,101):
                url = base_url.format(str(i))
                req = scrapy.Request(url=url,callback=self.parse)
                yield req

    def parse(self, response):
        res_dict = json.loads(response.body.decode('utf-8'))
        data_dict_list = res_dict['listItem']
        # print(len(data_dict_list))
        item = TaobaoItem()
        for data_dict in data_dict_list:

            item['title'] = data_dict['title']
            item['originalprice'] = data_dict['originalPrice']
            item['price'] = data_dict['price']
            item['nick'] = data_dict['nick']
            item['area'] = data_dict['area']
            item['pic_path'] = data_dict['pic_path']
            item['sold'] = data_dict['sold']
            yield item
