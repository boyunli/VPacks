#!/usr/bin/env python
# encoding: utf-8

保存图片:
import requests
import shutil

res = requests.get(img_url, stream=True)
if res .status_code == 200:
    with open('code.jpeg', 'wb') as ff:
        res.raw.decode_content = True
        shutil.copyfileobj(res.raw, ff)

