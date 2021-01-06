import functools
import time

CACHE = {}

def cache_it(func):
    @functools.wraps(func)