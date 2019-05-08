# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
from picDownload.items import PicDownloadItem
from decimal import Decimal


class PicDownloadSpider(Spider):
    name = 'pixabay'
    allowed_domains = ['pixabay.com']
    offset = 1
    start_urls = ['https://pixabay.com/images/search/?pagi='+str(offset)]

    def parse(self, response):
        urls = response.xpath('//div[@class="item"]/a/@href').extract()
        for url in urls:
            url_prefix_domain = 'https://pixabay.com'
            yield scrapy.Request(url_prefix_domain + url, callback=self.parse_item)
        self.offset += 1
        yield scrapy.Request('https://pixabay.com/images/search/?pagi=' + str(self.offset), callback=self.parse)

    def parse_item(self, response):
        item = PicDownloadItem()
        url = response.url
        newUrl = url[0:-1]
        item['image_name'] = newUrl[newUrl.rfind("/") + 1:]
        item['image_link'] = response.xpath('//div[@id="media_container"]/img[@itemprop="contentURL"]/@src').extract()[0]
        yield item
