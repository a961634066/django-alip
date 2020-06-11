# -*- coding:utf-8 -*-
import uuid

from alipay import AliPay
from urllib.request import urlopen
import os

from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from rest_framework.views import APIView

from zhifubao import constant


alipay = AliPay(appid=constant.appid, app_notify_url="http://127.0.0.1:8000/checkpay",
                alipay_public_key_string=constant.get_key()[0],
                app_private_key_string=constant.get_key()[1],debug=True)

class TradePay(APIView):

    def post(self, request):
        # 商户订单号,64个字符以内、可包含字母、数字、下划线；需保证在商户端不重复
        out_trade_no = uuid.uuid4().int
        print(out_trade_no)
        # 订单总金额，单位为元，精确到小数点后两位，取值范围[0.01,100000000]
        money = request.POST.get("money")
        # 订单标题
        subject = "淘宝网"
        # 订单包含的商品列表信息，json格式，其它说明详见商品明细说明
        # goods_id 商品的编号
        goods_detail = {"goods_id": "15825463123645", "goods_name": "橡皮", "quantity": 1, "price": 100}
        # 订单描述
        body = "Iphone6 16G"
        params = alipay.api_alipay_trade_page_pay(subject=subject,out_trade_no=out_trade_no,total_amount=money,
                                                  return_url="http://127.0.0.1:8000/checkpay",
                                                  notify_url="http://127.0.0.1:8000/checkpay",
                                                  body=body)
        print(params)
        return HttpResponseRedirect(constant.dev+"?"+params)
        # return JsonResponse({"status": 0, "msg": "ok", "req_url": constant.dev+params})

    # 主动查询订单状态
    def get(self, request):
        #  订单支付时传入的商户订单号,和支付宝交易号不能同时为空。
        # trade_no,out_trade_no如果同时存在优先取trade_no
        out_trade_no = "61785936312775849276631057629513884985"
        ret = alipay.api_alipay_trade_query(out_trade_no=out_trade_no)
        print(ret.trade_status)
        return HttpResponse(ret)

    # 退款
    def delete(self, request):
        out_trade_no = "53674439865466561806665338739669188099"
        ret = alipay.api_alipay_trade_refund(refund_amount="1",out_trade_no=out_trade_no)
        if ret.get("code") != '10000':
            print(ret)
            return HttpResponse(ret.get("sub_msg"))
        print(ret)
        return HttpResponse("退款成功")