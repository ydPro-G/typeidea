import time

CACHE = {}

def query(sql):
    try:
        result = CACHE[sql]
    except KeyError:
        time.sleep(5)
        result = 'execute %s' % sql
        CACHE[sql] = result
    return result

if __name__ == '__main__':
    start = time.time()
    query('SELETE * FROM blog_post')
    print(time.time() - start)

    start = time.time()
    query('SELECT * FROM blog_post')
    print(time.time() - start)
