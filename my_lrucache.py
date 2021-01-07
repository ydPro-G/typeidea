import time
from collections import OrderedDict

# 实现一个dict，设定好淘汰算法--淘汰掉最长时间没使用的那个。

class LRUCacheDict:
    def __init__(self, max_size=1024, expiration=60):
        """最大容量为1024个key，每个key的有效期为60S"""
        self.max_size = max_size
        self.expiration = expiration

        self._cache = {}
        self._access_records = OrderedDict() # 记录访问时间
        self._expire_records = OrderedDict() # 记录失效时间
    
    # 项目集合
    def __setitem__(self, key, value):
        now = int(time.time())
        self.__delete__(key)

        self._cache[key] = value
        self._expire_records[key] = now + self.expiration
        self._access_records[key] = now

        self.cleanup()
    
    # 项目获取
    def __getitem__(self, key):
        now = int(time.time())
        del self._access_records[key]
        self._access_records[key] = now
        self.cleanup()

        return self._cache[key]
    
    # 执行完清扫任务后，返回key值
    def __contains__(self, key):
        self.cleanup()
        return key in self._cache

    # 删除函数
    def __delete__(self, key):
        if key in self._cache:
            del self._cache[key]
            del self._expire_records[key]
            del self._access_records[key]
    
    def cleanup(self):
        """
        去掉无效(过期或者超出存储大小)的缓存
        """
        if self.expiration is None:
            return None
        pending_delete_keys = []
        now = int(time.time())
        # 删除已经过期的缓存
        for k, v in self._expire_records.items():
            if v < now:
                pending_delete_keys.append(k)
        
        for del_k in pending_delete_keys:
            self.__delete__(del_k)
        
        # 如果数据量大于max_size,则删掉最旧的缓存
        while (len(self._cache) > self.max_size):
            for k in self._access_records:
                self.__delete__(k)
                break

if __name__ == '__main__':
    cache_dict = LRUCacheDict(max_size=2, expiration=10)
    cache_dict['name'] = 'one'
    cache_dict['age'] = 30
    cache_dict['addr'] = 'beijing'

    print('name' in cache_dict) # 输出False，因为容量是2，第一个key会被删掉
    print('age' in cache_dict) # 输出True

    time.sleep(11)

    print('age' in cache_dict) # 输出False，因为缓存失效了
    