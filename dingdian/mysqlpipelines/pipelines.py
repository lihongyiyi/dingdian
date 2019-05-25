# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .sql import Sql
from dingdian.items import DingdianItem
from dingdian.items import DChapterContentItem

class DingdianPipeline(object):

    def process_item(self, item, spider):
        print("=============DingdianPipeline.process_item=============")
        if isinstance(item, DingdianItem):
            novel_id = item['novel_id']
            list = Sql.select_by_novel_id(novel_id)

            if list : #if list不要写成len(list), 因为如果查不到返回的类型是NoneType, 具体原因待查
                print("已经存在了，vovel_id=", novel_id)
                pass
            else:
                name = item['name']
                author = item['author']
                novelurl = item['novelurl']
                serialnumber = item['serialnumber']
                serialstatus = item['serialstatus']
                category = item['category']
                novel_id = item['novel_id']

                Sql.insert_tb_novel(name, author,novelurl,serialnumber, serialstatus,category, novel_id)
                print("保存小说概要信息")

        if isinstance(item, DChapterContentItem):
                print("=============DChapterContentItem.process_item=============")
                novel_id = item['novel_id']
                chapter_name = item['chapter_name']
                chapter_url = item['chapter_url']
                chapter_content = item['chapter_content']
                chapter_num = item['chapter_num']

                Sql.insert_novel_chapter(novel_id, chapter_name, chapter_num, chapter_url, chapter_content)
                print("保存小说章节信息")
