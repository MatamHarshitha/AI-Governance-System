import json
from app.queue.client import redisclient
import redis

QueueName = "taskqueue"


redisclient = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
) 
def pushtask(taskdata: dict):
    print("Inside pushtask")
    taskjson = json.dumps(taskdata)

    redisclient.rpush(QueueName, taskjson)

    print("Task pushed to queue")
    print("Task pushed successfully")