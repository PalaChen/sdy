#!/usr/local/bin/python
# -*- coding:utf-8 -*-
# Author: jacky
# Time: 14-2-22 下午11:48
# Desc: 短信http接口的python代码调用示例
import http.client
import urllib.parse

# 服务地址
host = "sms.253.com"

# 端口号
port = 80

# 版本号
version = "v1.1"

# 查账户信息的URI
balance_get_uri = "/msg/balance"

# 智能匹配模版短信接口的URI
sms_send_uri = "/msg/send"

# 创蓝账号
un = "N1110757"

# 创蓝密码
pw = "f4VOD3Iius2090"


def get_user_balance():
    """
    取账户余额
    """
    conn = http.client.HTTPConnection(host, port=port)
    conn.request('GET', balance_get_uri + "?un=" + un + "&pw=" + pw)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str


def send_sms(text, phone):
    """
    能用接口发短信
    """
    params = urllib.parse.urlencode({'un': un, 'pw': pw, 'msg': text, 'phone': phone, 'rd': '1'})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection(host, port=port, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str


# if __name__ == '__main__':
#     phone = "13703077443"
#     text = "【253云通讯】您的验证码是1234"

    # 查账户余额
    # print(get_user_balance())

    # 调用智能匹配模版接口发短信
    # print(send_sms(text, phone))
