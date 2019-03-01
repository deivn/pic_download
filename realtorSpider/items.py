# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RealtorItem(scrapy.Item):
    click_url = scrapy.Field()
    status = scrapy.Field()
    # 城市名
    city_name = scrapy.Field()
    # city_id
    city_id = scrapy.Field()
    # 州ID
    state_id = scrapy.Field()
    # 邮编
    zip = scrapy.Field()
    # 街道信息
    street = scrapy.Field()
    # city_id
    # cityId = scrapy.Field()
    # 风格 公寓 还是个人
    house_type_name = scrapy.Field()
    # 经济人
    agent_name = scrapy.Field()
    base_info = scrapy.Field()
    price = scrapy.Field()
    beds = scrapy.Field()
    baths = scrapy.Field()
    living_sqft = scrapy.Field()
    # 图片列表
    pics = scrapy.Field()
    # 描述
    des = scrapy.Field()
    # build_year
    year_build = scrapy.Field()
    # 地段面积
    lot_size = scrapy.Field()
    # contactphone
    phone = scrapy.Field()
    # 用户ID
    uid = scrapy.Field()
    # 房源ID
    house_id = scrapy.Field()
    # house_type_id
    house_type_id = scrapy.Field()
    # 房源图片ID
    house_pic_id = scrapy.Field()
    # pic辅图的遍历
    pic = scrapy.Field()
