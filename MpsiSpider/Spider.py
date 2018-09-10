#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/9/009 23:26
# @Author  : Woe
# @Site    : 
# @File    : Spider.py
# @Software: PyCharm

from MpsiSpider.Consumer import BaseTask
from multiprocessing import cpu_count, Manager, Pool, freeze_support
from MpsiSpider.Producer import Producer


class Meta(type):
    # 把自动构建的类同一放入_fields
    def __new__(cls, name, bases, attrs):
        _fields = dict({(field_name, attrs.pop(field_name)) for field_name, object in list(attrs.items()) if
                        isinstance(object, BaseTask)})  ##
        attrs['_fields'] = _fields

        new_class = super(Meta, cls).__new__(cls, name, bases, attrs)
        return new_class


class Spider(metaclass=Meta):
    def __init__(self):
        self.requests_queue = Manager().Queue()
        self.Midle_queue = Manager().Queue()

    def start(self, pool_count=cpu_count()):

        freeze_support()
        # 此处field 既 topic
        pool = Pool(pool_count)

        for field in self._fields:
            for i in self._fields[field].urls:
                self.requests_queue.put((i, field))

        pool.apply_async(Producer(self.requests_queue, self.Midle_queue).scan_queue)
        for i in range(pool_count - 1):
            pool.apply_async(BaseTask.consumer_html,
                             kwds={'queue': self.Midle_queue, 'requests_queue': self.requests_queue,
                                   'fields': self._fields})

        pool.close()
        pool.join()
