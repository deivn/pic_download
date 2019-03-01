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
    offset = 1
    start_urls = ['https://www.realtor.com/realestateandhomes-search/Las-Vegas_NV']

    # rules = (
    #     Rule(LinkExtractor(allow=r'/realestateandhomes-search/Las-Vegas_NV/pg-\d+')),
    #     Rule(LinkExtractor(allow=r'/realestateandhomes-detail/\d+'), callback='parse_item'),
    # )
    def parse(self, response):
        urls = response.xpath('//div[@id="srp-list"]//ul//div[@data-label="property-photo"]/a/@href').extract()
        for url in urls:
            url_prefix_domain = 'https://www.realtor.com'
            yield scrapy.Request(url_prefix_domain + url, callback=self.parse_item, dont_filter=True)
        if self.offset <= 202:
            self.offset += 1
            yield scrapy.Request("https://www.realtor.com/realestateandhomes-search/Las-Vegas_NV/pg-" + str(self.offset), callback=self.parse)

    def parse_item(self, response):
        print(response.body)
        item = RealtorItem()
        item['click_url'] = response.url
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
        lot_size = house_info.xpath('./li[@data-label="property-meta-lotsize"]/span/text()').extract()[0].replace(",", "")
        lot_size_unit = house_info.xpath('./li[@data-label="property-meta-lotsize"]/text()').extract()[1].replace("\n", "").replace(" ", "")
        if lot_size_unit.find("sqft", 0, len(lot_size_unit)) > -1:
            item['lot_size'] = lot_size
        elif lot_size_unit.find('acres', 0, len(lot_size_unit)) > -1:
            item['lot_size'] = str(Decimal(lot_size) * Decimal(43560))
        else:
            print(lot_size_unit)

        # 类型、建造时间、房屋状态
        # 类型
        item['house_type_name'] = response.xpath('//div/li[@data-label="property-type"]//div/@data-original-title').extract()[0]
        # 建造时间
        item['year_build'] = response.xpath('//div/li[@data-label="property-year"]//div[2]/text()').extract()[0]
        # 房屋状态  Active还是其他状态，根据Active为在线状态
        item['status'] = response.xpath('//div/li[@class="ldp-key-fact-item"]/div/@data-original-title').extract()[0]
        # 代理经济人
        item['agent_name'] = response.xpath('//div[@class="row"]//div[@class="business-card-content"]//a[@data-label="additional-agent-name"]/text()').extract()[0]
        # phone
        item['phone'] = response.xpath('//div[@class="row"]//div[@class="business-card-content"]//li[@class="link-secondary"]/span/text()').extract()[0]
        # 街道信息
        # item['street'] = response.xpath('//div[@itemprop="name"]/@content').extract()[0]
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
