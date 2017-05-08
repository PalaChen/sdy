import types
# from urllib import urlencode, urlopen
from urllib.request import urlopen
from urllib.parse import urlencode
# from .hashcompact import md5_constructor as md5  # 见hashcompact.py
from .config import settings  # 见config.py


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
        k = smart_str(k, settings.ALIPAY_INPUT_CHARSET)
        if k not in ('sign', 'sign_type') and v != '':
            newparams[k] = smart_str(v, settings.ALIPAY_INPUT_CHARSET)
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
def create_direct_pay_by_user(tn, subject, body, bank, total_fee):
    params = {}
    params['service'] = 'create_direct_pay_by_user'
    params['payment_type'] = '1'  # 商品购买，只能选这个

    # 获取配置文件
    params['partner'] = settings.ALIPAY_PARTNER
    params['seller_id'] = settings.ALIPAY_PARTNER
    params['seller_email'] = settings.ALIPAY_SELLER_EMAIL
    params['return_url'] = settings.ALIPAY_RETURN_URL
    params['notify_url'] = settings.ALIPAY_NOTIFY_URL
    params['_input_charset'] = settings.ALIPAY_INPUT_CHARSET
    # params['show_url'] = settings.ALIPAY_SHOW_URL

    # 从订单数据中动态获取到的必填参数
    params['out_trade_no'] = tn[0]  # 请与贵网站订单系统中的唯一订单号匹配
    params['subject'] = subject[0]  # 订单名称，显示在支付宝收银台里的“商品名称”里，显示在支付宝的交易管理的“商品名称”的列表里。
    params['body'] = body[0]  # 订单描述、订单详细、订单备注，显示在支付宝收银台里的“商品描述”里，可以为空
    params['total_fee'] = total_fee  # 订单总金额，显示在支付宝收银台里的“应付总额”里，精确到小数点后两位
    # 扩展功能参数——网银提前
    if bank == 'alipay' or bank == '':
        params['paymethod'] = 'directPay'  # 支付方式，四个值可选：bankPay(网银); cartoon(卡通); directPay(余额); CASH(网点支付)
        params['defaultbank'] = ''  # 支付宝支付，这个为空
    else:
        params['paymethod'] = 'bankPay'  # 默认支付方式，四个值可选：bankPay(网银); cartoon(卡通); directPay(余额); CASH(网点支付)
        params['defaultbank'] = bank  # 默认网银代号，代号列表见http://club.alipay.com/read.php?tid=8681379

    params, prestr = params_filter(params)
    params['sign'] = build_mysign(prestr, settings.ALIPAY_KEY, settings.ALIPAY_SIGN_TYPE)
    params['sign_type'] = settings.ALIPAY_SIGN_TYPE

    return _GATEWAY + urlencode(params)


# 支付成功后验证是否是支付宝发来的通知
def notify_verify(post):
    # 初级验证--签名
    _, prestr = params_filter(post)
    mysign = build_mysign(prestr, settings.ALIPAY_KEY, settings.ALIPAY_SIGN_TYPE)

    if mysign != post.get('sign'):
        return False

    # 二级验证--查询支付宝服务器此条信息是否有效
    params = {}
    params['partner'] = settings.ALIPAY_PARTNER
    params['notify_id'] = post.get('notify_id')

    gateway = 'https://mapi.alipay.com/gateway.do?service=notify_verify&'

    verify_result = urlopen(gateway, urlencode(params).encode('utf-8')).read().decode('utf-8')
    if verify_result.lower().strip() == 'true':
        return True
    return False
