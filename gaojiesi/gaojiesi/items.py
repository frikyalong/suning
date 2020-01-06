# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GaojiesiItem(scrapy.Item):
    # define the fields for your item here like:
    cmmdtyCode = scrapy.Field()
    area_code = scrapy.Field()
    area_name = scrapy.Field()
    date = scrapy.Field()
    price = scrapy.Field()
    vendorName = scrapy.Field()
    shoppingCart = scrapy.Field()
    snPrice = scrapy.Field()
    refPrice = scrapy.Field()
    discount = scrapy.Field()
    originalPrice = scrapy.Field()
    bigPromotion = scrapy.Field()
    shoppingAllowance = scrapy.Field()
    promotionList = scrapy.Field()
