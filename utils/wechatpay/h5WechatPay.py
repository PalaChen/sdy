# -*- coding:utf-8 -*-

from wechatpay import WeChatPay


class H5WechatPay(WeChatPay):
    def __init__(self):
        self.params['trade_type'] = 'MWEB'
        self.params['scene_info'] = {
            "h5_info": {"type": "Wap", "wap_url": "http://www.shengdeye.com/wap", "wap_name": "盛德业"}}
