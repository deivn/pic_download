# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
from realtorSpider.items import RealtorItem
from decimal import Decimal


class RealtorSpider(Spider):
    name = 'realtor'
    allowed_domains = ['realtor.com']
    offset = 35
    start_urls = ['https://www.realtor.com/realestateandhomes-search/Las-Vegas_NV/pg-'+str(offset)]

    # rules = (
    #     Rule(LinkExtractor(allow=r'/realestateandhomes-search/Las-Vegas_NV/pg-\d+')),
    #     Rule(LinkExtractor(allow=r'/realestateandhomes-detail/\d+'), callback='parse_item'),
    # )
    def parse(self, response):
        urls = response.xpath('//div[@id="srp-list"]//ul//div[@data-label="property-photo"]/a/@href').extract()
        for url in urls:
            url_prefix_domain = 'https://www.realtor.com'
            yield scrapy.Request(url_prefix_domain + url, callback=self.parse_item, dont_filter=True)
        if self.offset <= 201:
            self.offset += 1
            yield scrapy.Request("https://www.realtor.com/realestateandhomes-search/Las-Vegas_NV/pg-" + str(self.offset), callback=self.parse)

    def parse_item(self, response):
        # print(response.body)
        item = RealtorItem()
        item['click_url'] = response.url
        # 来源
        # ss 'scrapy.http.headers.Headers'>
        # print(type(response.request.headers))
        item['referer'] = response.request.headers.get('Referer').decode(encoding='utf-8')
        pics = response.css('img::attr(data-src)').re('.*-w1020_h770_q80\.jpg')
        item['pics'] = list(set(pics))
        item['price'] = response.xpath('//div[@itemprop="offers"]/span[@itemprop="price"]/@content').extract()[0]
        house_info = response.xpath('//ul[@itemprop="description"]')
        item['beds'] = house_info.xpath('./li[@data-label="property-meta-beds"]/span/text()').extract()[0]
        full_half_baths_tmp = house_info.xpath('./li[@data-label="property-meta-baths"]')
        bath = house_info.xpath('./li[@data-label="property-meta-bath"]/span/text()').extract()
        if full_half_baths_tmp:
            full_half_baths = full_half_baths_tmp[0]
            full_bath = full_half_baths.xpath('./div[1]/span/text()').extract()[0]
            half_bath = full_half_baths.xpath('./div[2]/span/text()')
            if half_bath:
                item['baths'] = str(Decimal(full_bath) + Decimal(0.5))
            else:
                item['baths'] = full_bath
        elif bath:
            item['baths'] = bath[0]

        # 居住面积
        item['living_sqft'] = house_info.xpath('./li[@data-label="property-meta-sqft"]/span/text()').extract()[0].replace(",", "")
        # 占地面积
        lot_size_obj = house_info.xpath('./li[@data-label="property-meta-lotsize"]/span/text()')
        lot_size_unit_obj = house_info.xpath('./li[@data-label="property-meta-lotsize"]/text()')
        if lot_size_obj and lot_size_unit_obj:
            lot_size = lot_size_obj.extract()[0].replace(",", "")
            lot_size_unit = lot_size_unit_obj.extract()[1].replace("\n", "").replace(" ", "")
            if lot_size_unit.find("sqft", 0, len(lot_size_unit)) > -1:
                item['lot_size'] = lot_size
            elif lot_size_unit.find('acres', 0, len(lot_size_unit)) > -1:
                item['lot_size'] = str(Decimal(lot_size) * Decimal(43560))
        else:
            item['lot_size'] = '0'

        # 类型、建造时间、房屋状态
        # 类型
        item['house_type_name'] = response.xpath('//div/li[@data-label="property-type"]//div/@data-original-title').extract()[0]
        # 建造时间
        year_build = response.xpath('//div/li[@data-label="property-year"]//div[2]/text()')
        if year_build:
            item['year_build'] = year_build.extract()[0]
        else:
            item['year_build'] = ''
        # 房屋状态  Active还是其他状态，根据Active为在线状态
        item['status'] = response.xpath('//div/li[@class="ldp-key-fact-item"]/div/@data-original-title').extract()[0]
        # 代理经济人
        agent_name_first = response.xpath('//div[@class="row"]//div[@class="business-card-content"]//a[@data-label="additional-agent-name"]/text()')
        agent_name_second = response.xpath('//div[@class="row"]//div[@class="business-card-content"]//span[@data-label="additional-agent-name"]/text()')
        agent_name_three = response.xpath('//div[@class="row"]//div[@class="content"]//a[@data-label="additional-agent-name"]/text()')
        agent_name_forth = response.xpath('//div[@class="row"]//div[@class="content"]//a[@data-label="additional-agent-name"]/text()')
        if agent_name_first:
            item['agent_name'] = agent_name_first.extract()[0]
        elif agent_name_second:
            item['agent_name'] = agent_name_second.extract()[0]
        elif agent_name_three:
            item['agent_name'] = agent_name_three.extract()[0].replace("\n", "").strip()
        elif agent_name_forth:
            item['agent_name'] = agent_name_forth.extract()[0].replace("\n", "").strip()
        else:
            item['agent_name'] = ''
            print('none')
        # phone
        phone_first_env = response.xpath('//div[@class="row"]//div[@class="business-card-content"]//li[@class="link-secondary"]/span/text()')
        phone_second_env = response.xpath('//li[@class="link-secondary"]/span[@data-label="additional-office-phone"]/text()')
        if phone_first_env:
            item['phone'] = phone_first_env.extract()[0]
        elif phone_second_env:
            item['phone'] = phone_second_env.extract()[0].replace("\n", "").strip()
        else:
            item['phone'] = ''

        # 街道信息
        street = response.xpath('//div[@itemprop="name"]/@content').extract()[0]
        fields_temp  = street.split(",")
        item['street'] = fields_temp[0] + ','+fields_temp[1].lstrip()+','+fields_temp[2]
        # 1456 Macdonald Ranch Dr, Las Vegas, NV 89012
        fields = street.strip().split(',')
        item['city_name'] = fields[1].strip()
        cityid_zip = fields[2].strip().split()
        item['state_id'] = cityid_zip[0]
        item['zip'] = cityid_zip[1]
        des_1 = response.xpath('//div[@class="panel-body"]//p[@class="description"]/text()')
        des_2 = response.xpath('//p[@class="word-wrap-break"]/text()')
        if des_1:
            item['des'] = des_1.extract()[0]
        elif des_2:
            item['des'] = des_2.extract()[0]

        yield item
