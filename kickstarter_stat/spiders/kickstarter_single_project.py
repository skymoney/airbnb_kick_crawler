#-*- coding:utf-8 -*-

import scrapy

class KickstarterProjectWidgetSpider(scrapy.Spider):
    name = "kick_widget"

    allowed_domains = ['']

    start_urls = []
    
    def parse(self, response):
        pass
