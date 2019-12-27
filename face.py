#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-12-19 16:54
# @Author  : Shark
# @Site    : 
# @File    : faceai.py
# @Software: PyCharm

import face_recognition


def compare(origin, current):
    known_image = face_recognition.load_image_file(origin)
    unknown_image = face_recognition.load_image_file(current)

    biden_encoding = face_recognition.face_encodings(known_image)[0]
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

    results = face_recognition.face_distance([biden_encoding], unknown_encoding)
    return results[0]


# 检测是否含有人脸
def check(face_img):
    img = face_recognition.load_image_file(face_img)
    # top, right, bottom, left
    face_locations = face_recognition.face_locations(img, model='cnn')
    check = True
    if len(face_locations) == 0:
        check = False
        return {"check": check}
    else:
        return {"check": check, "location": face_locations[0]}