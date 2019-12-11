# -*- coding: utf-8 -*-
import scrapy
import time
from copy import deepcopy
from gaojiesi.items import GaojiesiItem
from gaojiesi.spiders.constant import area_codes, area_code_for_debug
from gaojiesi.spiders.utils import build_jsonp_urls, loads_jsonp


class SuningSpider(scrapy.Spider):
    name = 'suning'
    allowed_domains = ['suning.com']
    start_urls = ['http://suning.com/']

    def parse(self, response):
        keyword = "%E9%AB%98%E6%B4%81%E4%B8%9D"  # 高洁丝编码
        # ct=1 苏宁服务
        start_url_template = 'https://search.suning.com/emall/searchV1Product.do?keyword={}' \
                             '&ci=0&pg=01&cp=0&il=0&st=0&iy=0&hf=brand_Name_FacetAll:%E9%AB%98%E6%B4%81%E4%B8%9D' \
                             '&ct=1&isNoResult=0&n=1&sc=0&sesab=ACAABAABCAAA&id=IDENTIFYING&cc={}' \
                             '&paging={}&sub=0&jzq=69'
        item = GaojiesiItem()
        for area in area_codes:
            for i in range(4):
                area_code = area.get("id")
                if len(area_code) > 3:
                    area_code = area_code.lstrip('0')
                list_url = start_url_template.format(keyword, area_code, i)
                item['area_code'] = area_code
                item['area_name'] = area.get("name")
                yield scrapy.Request(
                    list_url,
                    callback=self.parse_sub_list,
                    meta={"item": deepcopy(item)}
                )

    def parse_sub_list(self, response):
        li_list = response.xpath("//li[@doctype='1']")
        item = response.meta['item']
        url_codes = []
        for li in li_list:
            def_price = li.xpath(".//span[@class='def-price']")
            product_id = def_price.xpath("./@datasku").extract_first().split('|||||')[0]
            cmmd_code = "{}{}".format((18 - len(product_id)) * '0', product_id)
            brand_id = def_price.xpath("./@brand_id").extract_first()
            threegroup_id = def_price.xpath("./@threegroup_id").extract_first()
            url_code = "{}____{}_{}".format(cmmd_code, threegroup_id, brand_id)
            url_codes.append(url_code)

        jsonp_urls = build_jsonp_urls(url_codes, item['area_code'])
        for jsonp_url in jsonp_urls:
            yield scrapy.Request(
                jsonp_url,
                callback=self.parse_detail,
                meta={"item": deepcopy(item)},
                dont_filter=True
            )

    def parse_detail(self, response):
        item = response.meta['item']
        obj = loads_jsonp(response.body.decode())
        if obj.get('message') is None and obj.get('status') == 200 and obj.get('rs') is not None:
            for result in obj.get('rs'):
                item['price'] = result.get('price')
                item['vendorName'] = result.get('vendorName')
                item['shoppingCart'] = "有货" if result.get('shoppingCart') == "1" else "缺货"
                item['cmmdtyCode'] = result.get('cmmdtyCode').lstrip('0')
                item['date'] = time.strftime("%Y-%m-%d", time.localtime())
                yield item



