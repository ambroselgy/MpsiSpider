from MpsiSpider.Request import Request
import asyncio
from MpsiSpider.utils import get_logger


class BaseTask(object):
    task_config = {
        'bitch_size': 10,
        'timehout': 5,
    }

    def __init__(self, urls):
        self.urls = urls

    def put_body(self, queue, urls=None):
        """

        :param queue:
        :param urls:
        :return:
        """
        if urls is None:
            urls = self.urls
        loop = asyncio.get_event_loop()

        async def request(url):
            res = await Request(url=url).fetch()
            queue.put_nowait(res)

        task = [asyncio.ensure_future(request(url=url)) for url in urls if url != 'end']
        loop.run_until_complete(asyncio.wait(task))

    @classmethod
    def get_body(self, queue: object) -> object:
        """

        :param queue:
        :return:
        """
        log = get_logger('Task')
        urls = ['end']
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()

        task = []
        while 1:
            try:
                res = queue.get(block=True, timeout=self.task_config['timehout'])
                task.append(asyncio.ensure_future(self.parse(res)))
                if len(task) > self.task_config['bitch_size']:
                    loop.run_until_complete(asyncio.wait(task))
                    for i in task:
                        if i.result():
                            urls.extend(i.result())
                    task = []
            except Exception as e:

                loop.run_until_complete(asyncio.wait(task))
                for i in task:
                    if i.result():
                        urls.extend(i.result())
                loop.close()
                log.info('the task end')
                return urls

    @classmethod
    async def parse(self, res):
        """
        解析网页并且返回需要继续抓取的网页
        :param res:
        :return: urls
        """
        pass
