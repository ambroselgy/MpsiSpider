#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/1/001 13:58
# @Author  : Woe
# @Site    : 
# @File    : test.py
# @Software: PyCharm


from MpsiSpider.Spider import Spider
from MpsiSpider.Task import BaseTask
if __name__ == '__main__':
    class aab(Spider):
        test = BaseTask(urls=['http://www.baidu.com','http://www.baidu.com','http://www.baidu.com','http://www.baidu.com','http://www.baidu.com','http://www.baidu.com','http://www.baidu.com','http://www.baidu.com','http://www.baidu.com','http://www.baidu.com','http://www.baidu.com','http://www.baidu.com','http://www.baidu.com','http://www.baidu.com','http://www.baidu.com','http://www.baidu.com'])
        pool_count = 4
    tt = aab()
    tt.start()

