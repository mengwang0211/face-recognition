#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : ${DATE} ${TIME}
# @Author  : Meng Wang
# @Site    : ${SITE}
# @File    : ${NAME}.py
# @Software: ${PRODUCT_NAME}


from elasticsearch import Elasticsearch, NotFoundError
import json
import traceback

f = open('es_config.json', 'r+')
str_json = f.read()
# 将 单引号 替换为 双引号
temp = str_json.replace("'", '"')
# loads 将 字符串 解码为 字典
temp = json.loads(temp)

es = Elasticsearch([temp['host']])


def insert(body):
    data = es.index(index="user_face", doc_type="user_face", body=body)
    return data


def selectAll():
    query = {'query': {'match_all': {}}}  # 查找所有文档
    return es.search(index="user_face", body=query)


def select(name):
    try:
        response = es.search(
            index="user_face",  # 索引名
            body={  # 请求体
                "query": {  # 关键字，把查询语句给 query
                    "bool": {  # 关键字，表示使用 filter 查询，没有匹配度
                        "must": [  # 表示里面的条件必须匹配，多个匹配元素可以放在列表里
                            {
                                "match": {  # 关键字，表示需要匹配的元素
                                    "user_name": name  # 是此字段需要匹配到的值
                                }
                            }]
                    }
                }
            }
        )
        return response
    except Exception as e:
        traceback.print_exc()
        return None