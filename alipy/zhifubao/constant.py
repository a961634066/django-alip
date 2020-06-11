# -*- coding:utf-8 -*-
import os

from alipy import settings

appid = "2016102200735776"
# 网关
dev = "https://openapi.alipaydev.com/gateway.do"
zhegshi = "https://openapi.alipay.com/gateway.do"

def get_key():
    f = open(os.path.join(settings.BASE_DIR, "zhifubao", "alipay_public.txt"))
    w = open(os.path.join(settings.BASE_DIR, "zhifubao", "app_privace.txt"))
    alipay_public_key_string = str(f.read())
    app_private_key_string = str(w.read())
    f.close()
    w.close()
    return alipay_public_key_string, app_private_key_string