# -*- coding: utf-8 -*-
import scrapy
import os
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString, Comment
from urllib import unquote


class NiukeSpider(scrapy.Spider):
    name = "niuke"
    filepos = ""

    def start_requests(self):
        start_url = 'https://www.zhihu.com/question/29693016/answer/123859334'
        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        for item in soup.find('div', id='zh-question-answer-wrap').find('div', class_='zm-editable-content').children:
            if isinstance(item, NavigableString):
                os.mkdir(item.string)
                self.filepos = item.string
                # print item.string
            else:
                if item.find('b'):
                    print 'b'
                    os.mkdir(item.get_text())
                    self.filepos = item.get_text()
                    continue
                target_source = item.find('a', class_='external')
                if target_source:
                    target_url = unquote(target_source['href']).replace('//link.zhihu.com/?target=', '')
                    yield scrapy.Request(url=target_url, callback=self.parse2, meta={'cat': self.filepos})
                # if not item.find('a', class_='external'):
                    # print item

    def parse2(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        filedir = response.meta['cat'] + '/'
        filename = filedir + soup.find('title').get_text().split('_')[0] + '.html'
        f = file(self.filepos.strip() + filename, 'w')
        f.write(response.body)
        f.close()
