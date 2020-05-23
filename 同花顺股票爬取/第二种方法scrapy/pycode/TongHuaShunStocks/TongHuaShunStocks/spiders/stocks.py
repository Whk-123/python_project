# -*- coding: utf-8 -*-
import scrapy
import requests
from bs4 import BeautifulSoup
import traceback
import re


class StocksSpider(scrapy.Spider):
    name = 'stocks'
    start_urls = []
    depth = int(input("输入要爬取的股票页数（1页20股，共188页）："))
    for i in range(depth):
        i += 1
        start_urls.append('http://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/'+str(i)+'/ajax/1/')

    # print("---"*200)
    # print(start_urls)
    # print("---" * 200)
    # start_urls = ['http://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/1/ajax/1/',
    #               'http://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/2/ajax/1/']


    def parse(self, response):
        infoDict = {}
        try:
            # 发现股票信息存放在tbody标签内
            stockInfo = response.css('tbody')

            # 一个tr标签对应一只股票
            valueList = stockInfo.css("tr")
            val = valueList.xpath("//tr/td/a/text() | //tr/td/text()").extract()
            # 定义列表keyList，用于匹配股票数据
            keyList = ["序号", "代码", "名称", "现价", "涨跌幅(%)", "涨跌", "涨速(%)", "换手(%)", "量比", "振幅(%)", "成交额", "流通股", "流通市值",
                       "市盈率"]

            # print(type(valueList))
            a = 0
            for i in range(len(valueList)):

                for x in range(len(keyList)):
                    key = keyList[a % 14]
                    # print(x)
                    infoDict[key] = val[a]
                    a += 1
                yield infoDict
                # print('--'*200)
                # print(a)        #14
                # print('--' * 200)
                # print(ilt)


        except:
            traceback.print_exc()
