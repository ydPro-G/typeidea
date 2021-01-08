import time
from my_lrucache import LRUCacheDict
import functools


# 引入自己写的字典 LRUCacheDict,

def cache_it(max_size=1024, expiration=60):
    CACHE = LRUCacheDict(max_size=max_size, expiration=expiration)

    def wrapper(func):
        # 保留原函数的签名
        @functools.wraps(func)
        def inner(*args, **kwargs):
            # 传递给它的对象都转为字符串
            key = repr(*args, **kwargs)
            try:
                result = CACHE[key]
            except KeyError:
                result = func(*args, **kwargs)
                CACHE[key] = result
            return result
        return inner
    return wrapper


@cache_it(max_size=10, expiration=3)
def query(sql):
    time.sleep(1)
    result = 'execute %s' %sql
    return result

if __name__ == '__main__':
    start = time.time()
    query('SELECT * FROM blog_post')
    print(time.time() - start)

    # 运行后第二次
    start = time.time()
    query('SELECT * FROM blog_post')
    print(time.time() - start)






