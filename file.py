#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/27 10:22 上午
# @Author  : Meng Wang
# @Site    : 
# @File    : file.py
# @Software: PyCharm

import base64
import time
import shutil
import os


# base64转 img
def baseb4__2__img(base64data):
    data = base64.b64decode(base64data)
    img_name = str(time.time()).replace('.', '') + "." + "jpg"
    with open(os.path.join('files/', img_name), 'wb') as f:
        f.write(data)
    shutil.copy(os.path.join('files/', img_name), os.path.join('filescopy/', img_name))
    return os.path.join('files/', img_name)
