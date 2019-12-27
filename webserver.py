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

from flask import Flask, request, render_template, redirect
import esquery
import face
from flask import request, send_from_directory, jsonify

import file

import logging
import traceback

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

LOG_PATH = 'logs'  # 设置log路径
LOG_FILE = 'api.log'  # 设置log文件名

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')

file_handler = logging.FileHandler("%s/%s" % (LOG_PATH, LOG_FILE))

# 可以通过setFormatter指定输出格式
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

logger.setLevel(logging.DEBUG)

__DEBUG = False

__DEFAULT__SCOPE = 0.5


# 提供接口供 SpringCloud 进行健康检查
@app.route("/health", methods=['GET'])
def health():
    logger.info("server health check")
    return jsonify(
        {"status": "UP"})


# 绑定访问地址127.0.0.1:5000/register
@app.route("/register", methods=['POST', 'GET'])
def register():
    logger.info("start register user")
    try:
        if request.method == 'POST':
            img = request.json["img"]
            name = request.json['userId']
            if select_by_name(name):
                imgFile = file.baseb4__2__img(img)
                check_res = face.check(imgFile)
                if check_res["check"] is False:
                    return jsonify(
                        {"code": 500, "message": "未检测到人脸"})
                else:
                    body = {"user_name": name, "img": imgFile}
                    data = esquery.insert(body)
                    location = check_res["location"]
                    user_face = {"faceToken": data["_id"],
                                 "location": {"left": location[3], "top": location[0], "width": location[1],
                                              "height": location[2]}}
                    return jsonify({"code": 0, "message": "Succeed", "data": user_face})
            else:
                return jsonify(
                    {"code": 500, "message": "该姓名已经被注册，请勿重复提交"})
    except Exception as ec:
        logger.error(traceback.format_exc())
        return exception__reponse()


# 绑定访问地址127.0.0.1:5000/check
@app.route("/check", methods=['POST', 'GET'])
def check():
    logger.info("start check user")
    try:
        if request.method == 'POST':
            img = request.json["img"]
            imgFile = file.baseb4__2__img(img)
            check_res = face.check(imgFile)
            if check_res["check"] is False:
                return jsonify(
                    {"code": 500, "message": "未检测到人脸"})
            else:
                userList = esquery.selectAll()
                items = userList['hits']['hits']
                reponseList = []
                for user in items:
                    item = user['_source']
                    origin = item["img"]
                    faceToken = user["_id"]
                    result = face.compare(origin, imgFile)
                    logger.info("相似度:" + str(float(1) - result))
                    if result < __DEFAULT__SCOPE:
                        scope = float(1) - result
                        reponseList.insert(0,
                                           {"faceToken": faceToken, "userId": item["user_name"], "score": scope * 100})
                if reponseList is not None and len(reponseList) > 0:
                    firstScope = reponseList[0]["score"]
                    count = 0
                    for r in reponseList:
                        if firstScope == r["score"]:
                            if count > 0:
                                reponseList.remove(r)
                            count = count + 1
                return jsonify(
                    {"code": 0, "message": "Succeed", "data": {"user_list": reponseList}})
    except Exception as e:
        logger.error(traceback.format_exc())
        return exception__reponse()


def exception__reponse():
    return jsonify({"code": 500, "message": "Unexpected error:" + traceback.format_exc(), "data": None})


def select_by_name(name):
    users = esquery.select(name)["hits"]["hits"]
    count = len(users)
    if count == 0:
        return True
    else:
        return False


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
