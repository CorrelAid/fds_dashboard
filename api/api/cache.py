import redis
import json
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_ADR = os.environ.get("REDIS_ADR")
REDIS_PORT = os.environ.get("REDIS_PORT")

r = redis.Redis(host=REDIS_ADR, port=REDIS_PORT, db=0)

REDIS_EXPIRE = os.environ.get("REDIS_EXPIRE")


def cache_handler(db, key, query_function, **kwargs):
    cache_key = key
    cache_entry = r.get(cache_key)

    if cache_entry:
        print("using cache")
        return json.loads(cache_entry)
    else:
        print("using db")
        query_result = query_function(db=db, **kwargs)
        r.set(cache_key, json.dumps(query_result, indent=4, sort_keys=False, default=str))
        r.expire(cache_key, REDIS_EXPIRE)
        return query_result
