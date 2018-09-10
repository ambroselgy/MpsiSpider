#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/9/009 23:01
# @Author  : Woe
# @Site    : 
# @File    : Producer.py
# @Software: PyCharm

import asyncio

from MpsiSpider.Request import Request
import threading
import time


class Producer:

    def __init__(self, requests_queue, mid_queue):
        """

        :param requests_queue:
        :param mid_res:
        """
        self.requests_queue = requests_queue
        self.mid_quque = mid_queue


    def scan_queue(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        while 1:
            count = {
                'update': int(time.time()),
                'num': 0
            }
            reques_list = []
            while 1:
                try:
                    if count['num'] > 30 or int(time.time()) - count['update'] > 1:
                        if reques_list == []:
                            break

                        async def request(item):
                            res = await Request(url=item[0]).fetch()
                            self.mid_quque.put_nowait((item[1], res))

                        task = [asyncio.ensure_future(request(item=item)) for item in reques_list]
                        loop.run_until_complete(asyncio.wait(task))
                        break

                    reques_list.append(self.requests_queue.get(block=True, timeout=1))
                    count['update'] = time.time()
                    count['num'] = count['num'] + 1
                except:
                    pass
