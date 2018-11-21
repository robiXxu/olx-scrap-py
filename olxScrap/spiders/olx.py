# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.loader import ItemLoader
from olxScrap.items import Ad

class OlxSpider(scrapy.Spider):
    name = 'olx'
    allowed_domains = ['olx.ro']

    def start_requests(self):
      start_urls = [
        'https://www.olx.ro/oferte/q-logitech-g910/'
      ]

      for url in start_urls:
        yield scrapy.Request(url=url, callback=self.parseListPage)
      
    def parseListPage(self, response):
      urls = []
      for link in response.css('a.linkWithHash'):
        urls.append(link.css('a::attr(href)').extract_first())
      for url in urls:
        yield self.navigate(url)

    def navigate(self, url):
      return scrapy.Request(url=url, callback=self.parseItemPage)

    def parseItemPage(self, response):
      il = ItemLoader(item=Ad(), response=response)
      il.add_css('title','div#offer_active h1')
      il.add_css('location','div#offer_active a.show-map-link')
      il.add_css('description', 'div#offer_active div#textContent')
      il.add_css('price', 'div#offer_active div.price-label')
      il.add_css('addedAt', 'div#offer_active em')
      images = []
      for img in response.css('div#offer_active div.tcenter.img-item'):
        images.append(img.css('img::attr(src)').extract_first())

      il.add_value('images', images)
      print il.load_item()
