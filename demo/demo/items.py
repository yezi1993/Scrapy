# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class TaobaoItem(scrapy.Item):
    # 标题
    title = scrapy.Field()
    # 原价
    originalprice = scrapy.Field()
    # 现价
    price = scrapy.Field()
    # 昵称
    nick = scrapy.Field()
    # 地址
    area = scrapy.Field()
    # 图片地址
    pic_path = scrapy.Field()
    # 付款人数
    sold = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = "INSERT INTO taobao (title,originalprice,price,nick,area,pic_path,sold) " \
                     "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        data = (self['title'],self['originalprice'],self['price'],self['nick'],self['area'],self['pic_path'],self['sold'])
        return (insert_sql, data)


class LiepinItem(scrapy.Item):
    # 标题
    title = scrapy.Field()
    # 薪资
    price = scrapy.Field()
    # 地址
    site = scrapy.Field()
    # 工作经验
    experience = scrapy.Field()
    # 学历
    education = scrapy.Field()
    # 发布时间
    time = scrapy.Field()
    # 详情
    description = scrapy.Field()
    # 来自那个网站
    website = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = "INSERT INTO zhaopin (title,price,site,experience,education,time,description,website) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        data = (self['title'],self['price'],self['site'],self['experience'],self['education'],self['time'],self['description'],self['website'])
        return (insert_sql, data)