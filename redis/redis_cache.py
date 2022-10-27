import datetime

import redis
from redis_lru import RedisLRU


client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache(expire_on=datetime.time(hour=8))
def power_cache(x, y):
    match y:
        case 0:
            return 1
        case 1:
            return x
        case n:
            return x * power_cache(x, y - 1)


def main():
    x = int(input("Enter x: "))
    y = int(input("Enter y: "))
    result = power_cache(x, y)
    print(f"{x}^{y} = {result}")


if __name__ == '__main__':
    main()
