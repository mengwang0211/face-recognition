#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-12-05 14:25
# @Author  : Shark
# @Site    :
# @File    : webserver.py
# @Software: PyCharm

"""

webserver


"""
import json
import sys
import time

from flask import Flask, request, render_template, redirect
import os
import esquery
import face
from flask import request, send_from_directory, jsonify
import shutil
import datetime

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

__DEBUG = False

__DEFAULT__SCOPE = 0.5


# 绑定访问地址127.0.0.1:5000/register
@app.route("/register", methods=['POST', 'GET'])
def register():
    try:
        if request.method == 'POST':
            start = datetime.datetime.now()
            img = request.files["img"]
            originName = img.filename
            prefix = originName[originName.index(".") + 1:(len(originName))]
            name = request.form['name']
            if select_by_name(name):
                img_name = str(time.time()).replace('.', '') + "." + prefix
                img.save(os.path.join('files/', img_name))
                shutil.copy(os.path.join('files/', img_name), os.path.join('filescopy/', img_name))
                if face.check(os.path.join('filescopy/', img_name)) is False:
                    end = datetime.datetime.now()
                    return json.dumps(
                        {"code": 500, "msg": "未检测到人脸", "processTime": ((end - start).microseconds) / 1000},
                        ensure_ascii=False)
                else:
                    body = {"user_name": name, "img": img_name}
                    esquery.insert(body)
                    end = datetime.datetime.now()
                    return json.dumps({"code": 0, "msg": "Succeed", "processTime": ((end - start).microseconds) / 1000},
                                      ensure_ascii=False)
            else:
                end = datetime.datetime.now()
                return json.dumps(
                    {"code": 500, "msg": "该姓名已经被注册，请勿重复提交", "processTime": ((end - start).microseconds) / 1000},
                    ensure_ascii=False)
    except Exception as e:
        print(e)
        return exception__reponse()


# 绑定访问地址127.0.0.1:5000/check
@app.route("/check", methods=['POST', 'GET'])
def check():
    if request.method == 'POST':
        start = datetime.datetime.now()
        img = request.files["img"]
        originName = img.filename
        prefix = originName[originName.index(".") + 1:(len(originName))]
        img_name = str(time.time()).replace('.', '') + "." + prefix
        img.save(os.path.join('files/', img_name))
        shutil.copy(os.path.join('files/', img_name), os.path.join('filescopy/', img_name))
        if face.check(os.path.join('filescopy/', img_name)) is False:
            end = datetime.datetime.now()
            return json.dumps(
                {"code": 500, "msg": "未检测到人脸", "processTime": ((end - start).microseconds) / 1000},
                ensure_ascii=False)
        else:
            userList = esquery.selectAll()
            items = userList['hits']['hits']
            reponseList = []
            for user in items:
                item = user['_source']
                origin = item["img"]
                result = face.compare(os.path.join('files/' + origin), os.path.join('files/' + img_name))
                print("相似度:" + str(float(1) - result))
                if result < __DEFAULT__SCOPE:
                    scope = float(1) - result
                    reponseList.insert(0, {"name": item["user_name"], "scope": scope})
            if reponseList is not None and len(reponseList) > 0:
                firstScope = reponseList[0]["scope"]
                count = 0
                for r in reponseList:
                    if firstScope == r["scope"]:
                        if count > 0:
                            reponseList.remove(r)
                        count = count + 1
            end = datetime.datetime.now()
            return json.dumps(
                {"code": 0, "msg": "Succeed", "data": reponseList,
                 "processTime": ((end - start).microseconds) / 1000},
                ensure_ascii=False)


def exception__reponse():
    return json.dumps({"code": 500, "msg": "Unexpected error:" + str(sys.exc_info()[0]), "data": None})


def select_by_name(name):
    users = esquery.select(name)["hits"]["hits"]
    count = len(users)
    if count == 0:
        return True
    else:
        return False


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)