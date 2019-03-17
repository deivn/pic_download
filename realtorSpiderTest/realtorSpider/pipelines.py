# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import os
from datetime import datetime
from scrapy.conf import settings
from realtorSpider.optutil import OptUtil
from realtorSpider.mysqlutil import MysqlHelper
from realtorSpider.dealopt import HouseImportOpt
import json


class RealtorspiderPipeline(object):

    def __init__(self):
        # data_path = OptUtil.gen_file()
        # self.filename = codecs.open(data_path, "w", encoding="utf-8")
        self.house_id = 18781
        self.house_type_id = 18781
        self.uid = 18795
        self.house_pic_id = 61953
        # 加载house_type 无级转列表
        self.house_types = list(MysqlHelper.get_all('select id, name from t_house_type', []))
        # 加载房源地址并去重
        # 加载联系人去重
        # self.phones = set()
        # phome_set = MysqlHelper.get_all('select phone from t_user', [])
        # if phome_set:
        #     for phone in phome_set:
        #         self.phones.add(phone[0])


        # 加载地址过滤
        # self.urls = set()
        # temp_urls = MysqlHelper.get_all('select url from click_url', [])
        # if temp_urls:
        #     for url in temp_urls:
        #         self.urls.add(url[0])

    def process_item(self, item, spider):
        url = item['click_url']
        # if url in self.urls:
        #     pass
        # else:
        # self.urls.add(url)
        # content = json.dumps(dict(item), ensure_ascii=False) + '\n'
        # self.filename.write(content)
        status = item['status']
        pics = item['pics']
        pic_len = len(pics)
        des = item['des']
        phone = item['phone']
        typename = item['house_type_name']
        typename = HouseImportOpt.get_column_field(typename)
        is_empty = True if des else False
        origin_req = (item['referer'], item['click_url'], pic_len, status, phone, typename, str(is_empty))
        req_sql, req_params = HouseImportOpt.get_sql_info_by_code(item, "click_url", 5, *origin_req)
        primary_key = MysqlHelper.insert(req_sql, req_params)
        if status and status == 'Active' and typename and pic_len and des and phone :
            # 查询city_id
            result = MysqlHelper.get_one('select id from t_city where city_ascii = %s', [item['city_name']])
            item['city_id'] = result[0]
            self.uid += 1
            # 用户信息表t_user-----------------------------------------
            item['uid'] = self.uid
            user_sql, user_params = HouseImportOpt.get_sql_info_by_code(item, "t_user", 1, ())
            count = MysqlHelper.insert(user_sql, user_params)
            # 房源类型表 t_house_type----------------------------------------

            house_type_id, house_type_name, is_belongs = self.get_house_type_id(typename)
            item['house_type_id'] = house_type_id
            # 数据库中房源类型表没有该类型，则插入
            if not is_belongs:
                item['house_type_name'] = house_type_name
                house_type_sql, house_type_params = HouseImportOpt.get_sql_info_by_code(item, "t_house_type", 2, ())
                count = MysqlHelper.insert(house_type_sql, house_type_params)

            # 房源表 t_houses-----------------------------------------------------
            self.house_id += 1
            item['house_id'] = self.house_id
            house_sql, house_params = HouseImportOpt.get_sql_info_by_code(item, "t_houses", 3, ())
            count = MysqlHelper.insert(house_sql, house_params)
            if count == 1:
                result = MysqlHelper.update('update click_url set house_id = %s where id = %s', [item['house_id'], primary_key])

            # 房源辅图表t_house_img -----------------------------------------------
            for pic in pics:
                self.house_pic_id += 1
                item['house_pic_id'] = self.house_pic_id
                item['pic'] = pic
                house_img_sql, house_img_params = HouseImportOpt.get_sql_info_by_code(item, "t_house_img", 4, ())
                count = MysqlHelper.insert(house_img_sql, house_img_params)
        return item

    def close_spider(self, spider):
        # self.filename.close()
        pass

    def get_house_type_id(self, type_name):
        for id, name in self.house_types:
            if type_name == name:
                return (id, name, True)
        else:
            self.house_type_id += 1
            self.house_types.append((self.house_type_id, type_name))
            return (self.house_type_id, type_name, False)

