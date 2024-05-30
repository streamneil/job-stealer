#!/usr/bin/env python
# encoding: utf-8

import requests, json
from utils.logger import log

def get_request(url, headers, params=None):
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        assert response.status_code == 200
        return json.loads(response.content.decode('utf-8'))
    except Exception as e:
        log('Request Error get_request, e:', str(e))
        return None

def post_request(url, headers=None, data=None, json_data=None):
    try:
        response = requests.post(url, headers=headers, data=data, json=json_data)
        assert response.status_code == 200
        return json.loads(response.content.decode('utf-8'))
    except Exception as e:
        log('Request Error post_request, e:', str(e))
        return None

def create_cookie_header(cookie_dict):
    # 将字典转换为cookie字符串
    cookie_string = '; '.join([f"{key}={value}" for key, value in cookie_dict.items()])
    return cookie_string