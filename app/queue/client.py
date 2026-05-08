import redis


QueueName = "taskqueue"
redisclient = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)