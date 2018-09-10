#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/9/009 23:27
# @Author  : Woe
# @Site    : 
# @File    : Consumer.py
# @Software: PyCharm

import asyncio

class response:
    def __init__(self,body,urls):
        self.body = body
        self.urls = urls

    def body(self):
        return self.body

    def urls(self):
        return self.urls

class BaseTask(object):
    task_config = {
        'bitch_size': 50,
        'timehout': 5,
    }

    def __init__(self, urls):
        self.urls = urls

    @classmethod
    def consumer_html(self, queue: object, requests_queue: object, fields: object) -> object:
        """
        :param queue:
        :return:
        """
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        task = []
        while 1:
            try:
                res = queue.get(block=True, timeout=self.task_config['timehout'])
                item = response(body=res[1],urls=requests_queue)
                task.append(asyncio.ensure_future(fields[res[0]].parse(item)))
                if len(task) > self.task_config['bitch_size']:
                    loop.run_until_complete(asyncio.wait(task))
                    task = []
            except Exception as e:
                if task != []:
                    loop.run_until_complete(asyncio.wait(task))

    @classmethod
    async def parse(self, res):
        """
        :param res: 返回的html
        :param requests_queue: 需要再进行解析的queue　参数为(url,topic)
        :return:
        """
        from MpsiSpider.utils.logger import get_logger
        logger = get_logger('Task')
        logger.error('please set parse (self,res)')
