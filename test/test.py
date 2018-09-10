#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/1/001 13:58
# @Author  : Woe
# @Site    : 
# @File    : test.py
# @Software: PyCharm


from MpsiSpider.Spider import Spider
from MpsiSpider.Consumer import BaseTask
import os


class testTask(BaseTask):
    pass

if __name__ == '__main__':
    class aab(Spider):
        test = testTask(urls=["http://www.baidu.com"])


    a = aab()
    a.start()


