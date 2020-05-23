# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class TonghuashunstocksPipeline(object):

    def process_item(self, item, spider):
        return item

class TonghuashunstocksInfoPipeline(object):
    def open_spider(self,spider):
        self.f = open('TonghuashunstocksInfo.txt','w')

    def close_spder(self,spider):
        self.f.close()

    def process_item(self,item,spider):
        try:
            line = str(dict(item)) + '\n'
            self.f.write(line)
        except:
            pass
        return item
