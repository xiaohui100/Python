#!/usr/bin/env python
# encoding: utf-8
"""
@file: dict_to_list.py
@time: 2020/3/24
@author: alfons
"""
import json


def get_flatten_index(*args):
    """获取平铺数据的key，使用 . 连接"""
    return '.'.join([a for a in args if a])


def flatten_data(data, index="", cache=None):
    """
    把数据铺平
    :param data: 数据可以是list或者dict
    :param index: key的前缀
    :param list cache: 用作缓存，传入的为空列表
    :return list[dict]: 返回list类型

    用法：
    input = {
      "lun_list": [
        {
          "m_path": "/dev/qdata/mpath-s01.3272.01.LUN12",
          "disks": [
            {
              "mapped_disk": "/dev/nvme4n1",
              "status": "active",
              "ib_ip": "172.16.128.66",
              "port": 3272
            },
            {
              "mapped_disk": "/dev/nvme20n1",
              "status": "active",
              "ib_ip": "172.16.128.65",
              "port": 3272
            }
          ],
          "m_status": "enabled",
          "size": "10G"
        }
      ]
    }

    output = list()
    flatten_data(data=input, cache=output)

    输出：
    output = [
        {
            "lun_list.disks.port": 3272,
            "lun_list.disks.ib_ip": "172.16.128.66",
            "lun_list.m_status": "enabled",
            "lun_list.disks.status": "active",
            "lun_list.disks.mapped_disk": "/dev/nvme4n1",
            "lun_list.m_path": "/dev/qdata/mpath-s01.3272.01.LUN12",
            "lun_list.size": "10G"
        },
        {
            "lun_list.disks.port": 3272,
            "lun_list.disks.ib_ip": "172.16.128.65",
            "lun_list.m_status": "enabled",
            "lun_list.disks.status": "active",
            "lun_list.disks.mapped_disk": "/dev/nvme20n1",
            "lun_list.m_path": "/dev/qdata/mpath-s01.3272.01.LUN12",
            "lun_list.size": "10G"
        }
    ]
    """
    if isinstance(data, list):
        cache_tmp = list()
        for i in data:
            flatten_data(i, index, cache_tmp)
        [c.update(t) for t in cache for c in cache_tmp]
        [cache.pop(0) for _ in range(len(cache))]
        cache.extend(cache_tmp)
    elif isinstance(data, dict):
        # 针对一个dict下多个list对象进行特殊处理
        func_list = list()  # 存放dict下的list对象列表
        func_dict = list()  # 存放dict其他数据对象的列表
        for key, value in data.iteritems():
            if isinstance(value, list):
                func_list.append([get_flatten_index(index, key), value])
            else:
                func_dict.append([get_flatten_index(index, key), value])

        cache_tmp = list()  # 临时存放归档数据的列表
        for v in func_list:
            cache_list_tmp = list()
            flatten_data(v[1], v[0], cache_list_tmp)
            cache_tmp.extend(cache_list_tmp)

        for v in func_dict:
            flatten_data(v[1], v[0], cache_tmp)

        cache.extend(cache_tmp)
    else:
        if cache:
            [c.update({index: data}) for c in cache if isinstance(c, dict)]
        else:
            cache.append({index: data})


with open("show_c.json", "r") as f:
    j = json.loads(f.read())
    cache = list()
    flatten_data(j, cache=cache)
    with open("show_c_old.json", "w") as f:
        f.write(json.dumps(cache, indent=4))
    # res_1 = parse_dict(j)
    pass
