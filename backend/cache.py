import time

_cache = {}
CACHE_DURATION = 60 * 30  # 30 minutes

def get_cache(key):
    if key in _cache:
        data, timestamp = _cache[key]
        if time.time() - timestamp < CACHE_DURATION:
            print(f"Cache hit: {key}")
            return data
    return None

def set_cache(key, data):
    _cache[key] = (data, time.time())
    print(f"Cache set: {key}")

def clear_cache():
    _cache.clear()
    print("Cache cleared")