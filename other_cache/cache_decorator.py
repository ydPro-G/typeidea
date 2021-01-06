import functools
import time
# 将缓存逻辑封装为函数


CACHE = {}

def cache_it(func):
    # 保留原函数的签名，因为被装饰的函数实际上对外暴露的是装饰器函数。
    @functools.wraps(func)
    def inner(*args, **kwargs):
        # repr() 函数将对象转化为供解释器读取的形式。
        key = repr(*args,**kwargs)
        try:
            result = CACHE[key]
        except KeyError:
            result = func(*args, **kwargs)
            CACHE[key] = result
        return result
    return inner

@cache_it
def query(sql):
    time.sleep(1)
    result = 'execute %s' % sql
    return result


if __name__ == '__main__':
    start = time.time()
    query('SELECT * FROM blog_post')
    print(time.time() - start)

    # 运行后第二次
    start = time.time()
    query('SELECT * FROM blog_post')
    print(time.time() - start)
