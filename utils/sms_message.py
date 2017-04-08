from utils import sms
from reposition import models
import random
import re


def send_verification_code(phone):
    verify_code = random.randint(0000, 9999)
    text = '本次操作的验证码为：{},30分钟内有效。如非您本人操作，请忽略该短信。如需帮助，请拨打客服电话：0757-22104040'.format(verify_code)
    try:
        res = sms.send_sms(text, phone).decode('utf-8')
        res_list = re.findall('\d+', res)
        id = models.Users.objects.filter(phone=phone).values_list('id').first()[0]

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
        return
