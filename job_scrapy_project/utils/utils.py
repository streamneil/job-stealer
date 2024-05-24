#!/usr/bin/env python
# encoding: utf-8

import requests,time, json

def get_request(url, headers, params=None):
    response = requests.get(url, params=params, headers=headers, timeout=10)
    assert response.status_code == 200
    return json.loads(response.content.decode('utf-8'))

def post_request(url, headers=None, data=None, json_data=None):
    response = requests.post(url, headers=headers, data=data, json=json_data)
    assert response.status_code == 200
    return json.loads(response.content.decode('utf-8'))

def create_cookie_header(cookie_dict):
    # 将字典转换为cookie字符串
    cookie_string = '; '.join([f"{key}={value}" for key, value in cookie_dict.items()])
    return cookie_string