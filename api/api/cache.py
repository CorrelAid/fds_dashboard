import redis
import json
import os

REDIS_ADR = os.environ.get("REDIS_ADR")
REDIS_PORT = os.environ.get("REDIS_PORT")

r = redis.Redis(host=REDIS_ADR, port=REDIS_PORT, db=0)

def cache_handler(db, key, query_function):

    cache_key = key
    cache_entry = r.get(cache_key)

    if cache_entry:
        print("using cache")
        return json.loads(cache_entry)
    else:
        print("using db")
        query_result = query_function(db)
        print(query_result)
        r.set(cache_key, json.dumps(query_result, indent=4, sort_keys=True, default=str))
        r.expire(cache_key, 60*60*12)
        return query_result

