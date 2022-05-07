from typing import Any

import redis
from rq import Queue

from config import cfg


class QueueFactory:
    queues = {'redis': Queue}

    @classmethod
    def get_queue(cls, name: str, conn: Any) -> Queue:
        return cls.queues[name](connection=conn)


redis_conn = redis.from_url(cfg.REDIS_URL)
redis_queue = QueueFactory.get_queue('redis', redis_conn)
