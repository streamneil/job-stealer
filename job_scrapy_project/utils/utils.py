#!/usr/bin/env python
# encoding: utf-8

import requests,time, json

def get_request(url, headers, params=None):
    if params is None:
        params = {}

    response = requests.get(url, params=params, headers=headers, timeout=10)
    assert response.status_code == 200
    _ = json.loads(response.content.decode())
    return _

def post_request(url, headers=None, body=None):
    if body is None:
        body = {}

    response = requests.post(url, headers=headers, json=body)
    assert response.status_code == 200
    return json.loads(response.text)

def create_cookie_header(cookie_dict):
    # 将字典转换为cookie字符串
    cookie_string = '; '.join([f"{key}={value}" for key, value in cookie_dict.items()])
    return cookie_string