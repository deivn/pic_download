#! /usr/bin/env python  
# -*- coding:utf-8 -*-
import math
import time
from realtorSpider.sqlutil import SqlUtil


class HouseImportOpt(object):

    def __init__(self):
        pass

    @staticmethod
    def get_sql_info_by_code(item, tab_name, code):
        """
        功能：根据表名，字段列表，生成sql语句
        :param tab_name: 表名
        :param item: 网页爬取的信息
        :return:
        """
        _fields = HouseImportOpt().get_fields_by_code(code)
        sql = SqlUtil.gen_sql_sql(tab_name, _fields)
        params = HouseImportOpt().get_params_by_user_item(item, code)
        return (sql, params)

    def get_fields_by_code(self, code):
        """
        功能：根据code生成对应表的字段列表
        :param code: 字段标识code =1（用户表） 2 房源类型表 3 房源表 4 房源辅图表
        :return:
        """
        _fields = []
        if code == 1:
            _fields = [
                'id', 'phone', 'email', 'password', 'nickname', 'firstname', 'middlename',
                'lastname', 'sex', 'orgin', 'head_url', 'status', 'type', 'email_status',
                'state_id', 'city_id', 'address', 'zip', 'hxusername', 'phone_area_code_id',
                'create_time'
            ]
        elif code == 2:
            _fields = ['id', 'name', 'is_enable', 'img_url', 'add_time']
        elif code == 3:
            _fields = ['id', 'user_id', 'state_id', 'city_name', 'city_id', 'house_type_id', 'price',
                       'property_price', 'apn', 'street', 'zip', 'bedroom', 'bathroom',
                       'lot_sqft', 'user_input_unit', 'living_sqft', 'latitude', 'longitude',
                       'year_build', 'img_url', 'remark', 'origin', 'release_type', 'check_status', 'shelf_status',
                        'contact_name', 'contact_phone', 'contact_email', 'create_time']
        elif code == 4:
            _fields = ['id', 'houses_id', 'img_url', 'level', 'type', 'create_time']
        return _fields

    def get_params_by_user_item(self, item, code):
        """
        功能：根据用户item生成数据库表的参数列表
        :param item:
        :param code:1用户表参数 2房源类型表参数 3 房源表参数 4 房源辅图表参数
        :param id: primary key
        :param ids: 房源数据里要用到各个要关联的外键ID
        :return:
        """
        params = []
        create_time = math.floor(time.time())
        if code == 1:
            # 当前时间 yyyy-MM-dd HH:mm:ss
            current_time = SqlUtil.gen_current_time()
            params = [item['uid'], item['phone'], ' ', ' ', ' ', ' ', ' ', ' ',
                      3, 1, ' ', 1, 1, 1, item['state_id'], item['city_id'],
                      item['street'], item['zip'], ' ', ' ', current_time]
        elif code == 2:
            # if_belongs = self.house_type_belongs(name)
            # 数据库没有
            # 取图片列表第一张
            img_url = item['pics'][0] if len(item['pics']) else ''
            params = [item['house_type_id'], item['house_type_name'], 1, img_url, create_time]
        elif code == 3:
            # 物业费无
            property_price = 0
            apn = ''
            # 占地面积  爬到的数据固定是英亩单位，这里转换为英尺sqft
            lot_sqft = item['lot_size']
            # 带单位的sqft
            user_input_unit = str(lot_sqft) + "sqft"
            # 纬度
            latitude = 0
            # 经度
            longitude = 0
            # origin 来源:1.pc,2.wap,3.ios,4.Android  这里统一成pc
            orgin = 1
            # release_type 发布类型:1.出售,2.整租，3合租 统一是出售
            release_type = 1
            # check_status 审核状态:1.审核中,2.已审核,3.审核失败
            check_status = 1
            # shelf_status 上架状态:1.上架,2.下架，3删除
            shelf_status = 1
            params = [item['house_id'], item['uid'], item['state_id'], item['city_name'], item['city_id'], item['house_type_id'],
                      item['price'], property_price, apn, item['street'], item['zip'], item['beds'], item['baths'],
                      lot_sqft, user_input_unit, item['living_sqft'], latitude, longitude,
                      item['year_build'], item['pics'][0], item['des'][0], orgin, release_type, check_status,
                      shelf_status, item['agent_name'], item['phone'], "", create_time
                      ]
        elif code == 4:
            params = [item['house_pic_id'], item['house_id'], item['pic'], 0, 1, create_time]
        return params

    @staticmethod
    def get_column_field(structure_type):
        if structure_type == 'Townhome':
            structure_type = 'Town house'
        elif structure_type == 'Multi':
            structure_type = 'Multiple'
        elif structure_type == 'Condo':
            structure_type = 'Condos/co-ops'
        elif structure_type == 'Farm':
            structure_type = 'Lots/Land'
        return structure_type
