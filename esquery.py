#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : ${DATE} ${TIME}
# @Author  : Meng Wang
# @Site    : ${SITE}
# @File    : ${NAME}.py
# @Software: ${PRODUCT_NAME}


from elasticsearch import Elasticsearch

es = Elasticsearch()


def insert(body):
    es.index(index="user_face", doc_type="user_face", body=body)


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
    except:
        return None;