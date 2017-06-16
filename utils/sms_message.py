from utils import sms
from reposition import models
import random
import re


def send_verification_code(phone, type):
    verify_code = random.randint(1001, 9999)
    text = '验证码为：{},30分钟内有效。如非您本人操作，请忽略该短信。如需帮助，请拨打客服电话：0757-22104040'.format(verify_code)
    try:
        res = sms.send_sms(text, phone).decode('utf-8')
        res_list = re.findall('\d+', res)
        if type == 'edit':
            id = models.Users.objects.filter(phone=phone).values_list('id').first()[0]
        else:
            id = ''

        models.MessagesVerifyCode.objects.create(m_status=res_list[1],
                                                 m_response_time=res_list[0],
                                                 m_messageid=res_list[2],
                                                 m_text=text,
                                                 m_phone=phone,
                                                 m_user_id=id,
                                                 m_verifycode=verify_code,
                                                 )
        return True
    except Exception as e:
        print('---------短信错误提示:', e)
        return


def process_message_send(order, step_name, employee_id):
    text = '用户您好，您的服务订单:{}，进度更新：{}；' \
           '如有疑问关注微信公众号DE0757咨询。'.format(order.order_code, step_name)
    # text = '【盛德业】用户您好，您的服务订单:{}，进度更新：{}；' \
    #        '如有疑问登陆m.shengdeye.com官网咨询。'.format(order.order_code, step_name[0])

    phone = order.phone
    # else:
    #     text = '龙泽金你好，用户账号{}没有手机号码，无法发送短信'.format(order.username)
    #     res = sms.send_sms(text, 15363626218)
    message = {
        'order_id': order.id,
        'phone': order.phone,
        'content': text,
        'employee_id': employee_id,
    }
    try:
        res = sms.send_sms(text, phone).decode('utf-8')
        print('res:', res)
        res_list = re.findall('\d+', res)
        message['response_time'] = res_list[0]
        message['status'] = res_list[1]
        message['message_id'] = res_list[2]
    except Exception as e:
        message['status'] = 127
        message['response_time'] = 0
        message['message_id'] = 0
    print('message:', message)
    models.MessagesSend.objects.create(**message)
