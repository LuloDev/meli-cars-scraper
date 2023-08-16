from redis import Redis
from rq import Queue

q = Queue(connection=Redis('127.0.0.1', 6379))
