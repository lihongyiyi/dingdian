# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from dingdian.items import DingdianItem
from dingdian.items import DChapterContentItem
import re


class DingdianxsSpider(scrapy.Spider):
    name = 'dingdianxs'
    allowed_domains = ['www.23us.so']
    start_urls = ['http://www.23us.so/']
    base_url = "https://www.23us.so/list/"
    url_suff = ".html"

    full_url = "https://www.23us.so/full.html"

    def start_requests(self):
        for i in range(1, 2):
            url = self.base_url + str(i) + '_1' +self.url_suff
            yield Request(url, self.parse, meta={"is_full": 0}) # 此处self.parse不能写成self.parse()
        yield Request(self.full_url, self.parse, meta={"is_full": 1}) # 此处self.parse不能写成self.parse()

    def parse(self, response):
        is_full_flag = response.meta['is_full']
        max_num = BeautifulSoup(response.text, 'lxml').find('div', class_='pagelink').find_all('a')[-1].get_text()
        if is_full_flag == 0:
            print("is_full_flag={},max_num={}".format(is_full_flag, max_num))
            baseurl = str(response.url)[:-7]
            for num in range(1, 3): # TODO 因为学习练习，max_num暂时改成2
                url = baseurl + '_' + str(num) + self.url_suff
                yield Request(url, callback=self.get_name, dont_filter=True) #不加dont_filter=True， 调不到get_name
        else:
            print("is_full_flag={},max_num={}".format(is_full_flag, max_num))
            fullBaseUrl = "https://www.23us.so/modules/article/articlelist.php?fullflag=1&page="
            for num in range(1, int(max_num)+1):
                url = fullBaseUrl + str(num)
                yield Request(url, callback=self.get_name, dont_filter=True)


    def get_name(self, response):
        print("==========get_name===============")
        trs = BeautifulSoup(response.text, 'lxml').find_all('tr', bgcolor='#FFFFFF')
        for tr in trs:
            novalname = tr.find('a').get_text()
            novalurl = tr.find('a')['href']
            yield Request(novalurl, callback=self.get_chapterurl, meta={'name':novalname, 'url': novalurl})

    def get_chapterurl(self, response):
        print("==========get_chapterurl===============")
        item = DingdianItem()
        chaptSoup = BeautifulSoup(response.text, 'lxml')

        item['name'] = response.meta['name'].replace(chr(0xa0),'')
        item['author'] = chaptSoup.find('table').find_all('td')[1].get_text().replace(chr(0xa0),'')
        item['novelurl'] = response.meta['url']
        item['serialnumber'] = chaptSoup.find('table').find_all('tr')[1].find_all('td')[1].get_text().replace(chr(0xa0),'')
        item['serialstatus'] = chaptSoup.find('table').find_all('tr')[0].find_all('td')[2].get_text().replace(chr(0xa0),'')
        item['category'] = chaptSoup.find('table').find('a').get_text()


        #latestChapterUrl = chaptSoup.find('p', class_='btnlinks').find('a', class_="read")['href']
        #item['novel_id'] = latestChapterUrl[-16:-11] 当id位数不一样时，有问题
        item['novel_id'] = int(re.findall(r"xiaoshuo/(.+?).html", item['novelurl'])[0])

        # 如果只需要实现以上的功能，必须有return，否则执行不到pipelines.py
        # return item

        yield item
        latestChapterUrl = chaptSoup.find('p', class_='btnlinks').find('a', class_="read")['href']
        yield Request(url=latestChapterUrl, callback=self.get_chapter, meta={"novel_id": item['novel_id']})

    def get_chapter(self, response):
        print("=================get_chapter===============")
        novel_id = response.meta['novel_id']

        # 返回列表，列表的元素是元祖：[('https://www.23us.so/files/article/html/26/26271/12425250.html', '第一章 战神重生'),...]
        chapter_urls = re.findall('<td class="L"><a href="(.*?)">(.*?)</a></td>', response.text)

        chapter_num = 0
        for url in chapter_urls:
            chapter_num += 1
            chapter_url = url[0]
            chapter_name = url[1]
            yield Request(chapter_url,
                          callback=self.get_chapter_content,
                          meta={"novel_id": novel_id,
                                "chapter_name": chapter_name,
                                "chapter_url": chapter_url,
                                "chapter_num": chapter_num
                                })

    def get_chapter_content(self, response):
        print("=================get_chapter_content===============")
        item = DChapterContentItem()

        item['novel_id'] = response.meta['novel_id']
        item['chapter_name'] = response.meta['chapter_name'].replace(chr(0xa0), '')
        item['chapter_url'] = response.meta['chapter_url']
        item['chapter_num'] = response.meta['chapter_num']

        contentSoup = BeautifulSoup(response.text, 'lxml')
        item['chapter_content'] = contentSoup.find('dd', id="contents").get_text()[:500].replace(chr(0xa0), '')

        return item
