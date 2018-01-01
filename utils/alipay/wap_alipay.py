import types
# from urllib import urlencode, urlopen
from urllib.request import urlopen
from urllib.parse import urlencode
from .config import URL

# from .hashcompact import md5_constructor as md5  # 见hashcompact.py

"""
配置信息
"""
# 安全检验码，以数字和字母组成的32位字符
ALIPAY_KEY = 'hx7qx6xur0vu51pj22izwyc0nj81qh8e'

ALIPAY_INPUT_CHARSET = 'utf-8'

# 合作身份者ID，以2088开头的16位纯数字
ALIPAY_PARTNER = '2088221542945392'

# 签约支付宝账号或卖家支付宝帐户
ALIPAY_SELLER_EMAIL = 'd0757@139.com'

ALIPAY_SIGN_TYPE = 'MD5'

# 付完款后跳转的页面（同步通知） 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
ALIPAY_RETURN_URL = 'http://{}/wap/alipay/return/'.format(URL)

# 交易过程中服务器异步通知的页面 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
ALIPAY_NOTIFY_URL = 'http://{}/wap/alipay/notify/'.format(URL)


# 字符串编解码处理
def smart_str(s, encoding='utf-8', strings_only=False, errors='strict'):
    if strings_only and isinstance(s, (types.NoneType, int)):
        return s
    if not isinstance(s, str):
        # if not isinstance(s, basestring):
        try:
            return str(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                return ' '.join([smart_str(arg, encoding, strings_only,
                                           errors) for arg in s])
            # return unicode(s).encode(encoding, errors)
            return s.encode(encoding, errors)
    # elif isinstance(s, unicode):
    #     return s.encode(encoding, errors)
    elif s and encoding != 'utf-8':
        return s.decode('utf-8', errors).encode(encoding, errors)
    else:
        return s


# 网关地址
_GATEWAY = 'https://mapi.alipay.com/gateway.do?'


# 对数组排序并除去数组中的空值和签名参数
# 返回数组和链接串
def params_filter(params):
    ks = list(params.keys())

    ks.sort()
    newparams = {}
    prestr = ''
    for k in ks:
        v = params[k]
        k = smart_str(k, ALIPAY_INPUT_CHARSET)
        if k not in ('sign', 'sign_type') and v != '':
            newparams[k] = smart_str(v, ALIPAY_INPUT_CHARSET)
            prestr += '%s=%s&' % (k, newparams[k])
    prestr = prestr[:-1]
    return newparams, prestr


# 生成签名结果
def build_mysign(prestr, key, sign_type='MD5'):
    if sign_type == 'MD5':
        import hashlib
        md5 = hashlib.md5()
        md5.update(bytes(prestr + key, encoding='utf-8'))
        auth_key = md5.hexdigest()
        return auth_key


# 即时到账交易接口
def create_direct_pay_by_user(tn, subject, body, total_fee):
    params = {}
    # 基本参数
    params['service'] = 'alipay.wap.create.direct.pay.by.user'  # 接口名称
    params['partner'] = ALIPAY_PARTNER  # 合作者身份ID
    params['_input_charset'] = ALIPAY_INPUT_CHARSET  # 参数编码字符集
    params['sign_type'] = ALIPAY_SIGN_TYPE

    # 业务参数
    params['payment_type'] = '1'  # 商品购买，只能选这个
    params['out_trade_no'] = tn[0]  # 请与贵网站订单系统中的唯一订单号匹配
    params['subject'] = subject[0]  # 订单名称，显示在支付宝收银台里的“商品名称”里，显示在支付宝的交易管理的“商品名称”的列表里。
    params['body'] = body[0]  # 订单描述、订单详细、订单备注，显示在支付宝收银台里的“商品描述”里，可以为空
    params['total_fee'] = total_fee  # 订单总金额，显示在支付宝收银台里的“应付总额”里，精确到小数点后两位
    params['app_pay'] = 'Y'  # app_pay=Y：尝试唤起支付宝客户端进行支付，若用户未安装支付宝，则继续使用wap收银台进行支付。
    params['sign_type'] = 'MD5',
    # 获取配置文件
    params['seller_id'] = ALIPAY_PARTNER
    # params['seller_email'] = ALIPAY_SELLER_EMAIL
    params['return_url'] = ALIPAY_RETURN_URL
    params['notify_url'] = ALIPAY_NOTIFY_URL

    # params['show_url'] = ALIPAY_SHOW_URL




    params, prestr = params_filter(params)
    # 必填参数 签名
    params['sign'] = build_mysign(prestr, ALIPAY_KEY, ALIPAY_SIGN_TYPE)

    return _GATEWAY + urlencode(params)


# 支付成功后验证是否是支付宝发来的通知
def notify_verify(post):
    # 初级验证--签名
    _, prestr = params_filter(post)
    mysign = build_mysign(prestr, ALIPAY_KEY, ALIPAY_SIGN_TYPE)

    if mysign != post.get('sign'):
        return False

    # 二级验证--查询支付宝服务器此条信息是否有效
    params = {}
    params['partner'] = ALIPAY_PARTNER
    params['notify_id'] = post.get('notify_id')

    gateway = 'https://mapi.alipay.com/gateway.do?service=notify_verify&'

    verify_result = urlopen(gateway, urlencode(params).encode('utf-8')).read().decode('utf-8')
    if verify_result.lower().strip() == 'true':
        return True
    return False
