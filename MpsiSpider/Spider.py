#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/1/001 14:17
# @Author  : Woe
# @Site    :
# @File    : Spider.py
# @Software: PyCharm


from MpsiSpider.utils import get_logger
from multiprocessing import cpu_count, freeze_support, Pool, Queue
from MpsiSpider.Task import BaseTask

from multiprocessing import Process, Pool, Queue, Manager


class Meta(type):

    # 把自动构建的类同意放入_fields
    def __new__(cls, name, bases, attrs):
        _fields = dict({(field_name, attrs.pop(field_name)) for field_name, object in list(attrs.items()) if
                        isinstance(object, BaseTask)})  ##
        attrs['_fields'] = _fields

        if 'pool_config' in attrs:
            pool_config = attrs['pool_count']
        else:
            pool_config = {
                'pool_count': cpu_count(),
                'requests_pool': int(cpu_count() / 3),
                'parse_pool': int(cpu_count() / 3 * 2)
            }
        attrs['pool_config'] = pool_config
        new_class = super(Meta, cls).__new__(cls, name, bases, attrs)
        return new_class


class Spider(metaclass=Meta):

    def start(self):
        log = get_logger('Spider')
        log.info('start the spider')

        pool = Pool(self.pool_config['pool_count'])

        for field in self._fields:
            urls = self._fields[field].urls

            queue = Manager().Queue()
            while urls:
                if urls[-1] == 'end':
                    break
                index = (len(urls))
                temp = 0
                for i in range(self.pool_config['requests_pool']):
                    if i != ((self.pool_config['requests_pool'] - 1)):
                        count = int(index / self.pool_config['requests_pool'] * (i + 1))
                    else:
                        count = index
                    pool.apply_async(self._fields[field].put_body, (queue, urls[temp:count]))
                    temp = count
                    if temp == index:
                        break

                urls = []
                for i in range(self.pool_config['parse_pool']):
                    pool.apply_async(self._fields[field].get_body, kwds={'queue': queue}, callback=urls.extend)

                pool.close()
                pool.join()  # 进程池中进程执行完毕后再关闭，如果注释，那么程序直接关闭。
                pool = Pool(self.pool_config['pool_count'])

        pool.close()
        pool.join()
