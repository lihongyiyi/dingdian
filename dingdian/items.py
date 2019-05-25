# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DingdianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 小说的名字
    name = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 小说地址
    novelurl = scrapy.Field()
    # 连载字数
    serialnumber = scrapy.Field()
    #状态
    serialstatus = scrapy.Field()
    # 文章类别
    category = scrapy.Field()
    # 小说编号
    novel_id = scrapy.Field()



class DChapterContentItem(scrapy.Item):
    # 小说编号
    novel_id = scrapy.Field()
    # 章节名称
    chapter_name = scrapy.Field()
    # 章节名称
    chapter_url = scrapy.Field()
    # 章节内容
    chapter_content = scrapy.Field()
    # 章节序号
    chapter_num = scrapy.Field()