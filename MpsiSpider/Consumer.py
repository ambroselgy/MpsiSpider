#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/9/009 23:27
# @Author  : Woe
# @Site    : 
# @File    : Consumer.py
# @Software: PyCharm

import asyncio
from MpsiSpider.utils import get_logger

import importlib


def dynamic_import(module):
    return importlib.import_module(module)


class BaseTask(object):
    task_config = {
        'bitch_size': 10,
        'timehout': 10,
    }

    def __init__(self, urls):
        self.urls = urls

    @classmethod
    def consumer_html(self, queue: object, requests_queue: object, fields: object) -> object:
        """
        :param queue:
        :return:
        """
        log = get_logger('Task')
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        task = []
        while 1:
            try:
                res = queue.get(block=True, timeout=self.task_config['timehout'])

                task.append(asyncio.ensure_future(fields[res[0]].parse(res[1], requests_queue)))
                if len(task) > self.task_config['bitch_size']:
                    loop.run_until_complete(asyncio.wait(task))
                    task = []
            except Exception as e:
                loop.run_until_complete(asyncio.wait(task))

    @classmethod
    async def parse(self, res, requests_queue):
        """

        :param res: 返回的html
        :param requests_queue: 需要再进行解析的queue　参数为(url,topic)
        :return:
        """
        # print(res)
        print(requests_queue.qsize())
        requests_queue.put(('http://www.baidu.com', 'test'))
        print(requests_queue.qsize())
