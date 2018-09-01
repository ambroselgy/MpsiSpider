from EasySpider.Request import Request
import asyncio


class BaseTask(object):

    def __init__(self, urls):
        self.urls = urls

    def put_body(self, queue, urls=None):
        if urls is None:
            urls = self.urls
        loop = asyncio.get_event_loop()

        async def request(url):
            res = await Request(url=url).fetch()
            queue.put_nowait(res.body)

        task = [asyncio.ensure_future(request(url=url)) for url in urls]
        loop.run_until_complete(asyncio.wait(task))

    @classmethod
    def get_body(self, queue: object) -> object:
        while 1:
            try:
                res = queue.get(block=True,timeout=3)
                print(res[0:3])
            except:
                break
        # loop = asyncio.get_event_loop()
        #
        #
        #
        #
        # async def parse_master(queue):
        # asyncio.ensure_future(parse_master())
        # try:
        #     loop.run_forever()
        # finally:
        #     pass
