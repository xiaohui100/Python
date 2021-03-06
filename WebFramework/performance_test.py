#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file: performance_test.py
@time: 2020/6/19
@author: alfons
"""
import time
import requests
from multiprocessing.pool import ThreadPool

REQUEST_GET = "get"
REQUEST_POST = "post"

total_num = 0


def func_request(method: str = REQUEST_GET, url: str = None, num: int = None):
    if method == REQUEST_GET:
        response = requests.get(url)
        global total_num
        total_num += 1
        print("{}: {}".format(num, response.content))


start_time = time.time()
with ThreadPool(100) as pool:
    for i in range(10 ** 2):
        pool.apply_async(func_request, (REQUEST_GET, f"http://127.0.0.1:8000/sync_ssh", i))
        # pool.apply_async(func_request, (REQUEST_GET, f"http://127.0.0.1:8000/async_ssh", i))
    # for i in range(10):
    #     pool.apply_async(func_request, (REQUEST_GET, "http://127.0.0.1:8000/?i=0", i))

    pool.close()
    pool.join()

print("\n\nTotal time use: {:.2f}'s.".format(time.time() - start_time))
print(f"Total number: {total_num}")
