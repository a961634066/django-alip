import uuid

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from zhifubao.alipay import AliPay

alipay = AliPay(appid="2016102200735776", app_notify_url="http://127.0.0.1:8000/checkpay",
                app_private_key_path=r"E:\工作区-刘博\alipy\zhifubao\app_privace.txt",
                alipay_public_key_path=r"E:\工作区-刘博\alipy\zhifubao\alipay_public.txt",
                return_url="http://127.0.0.1:8000/checkpay", debug=True)


def index_view(request):
    return render(request, "index.html")


# 获取支付宝二维码页面
def pay_view(request):
    money = request.POST.get("money", 10)
    # 获取扫码支付请求参数
    out_trade_no = uuid.uuid4().int
    params = alipay.direct_pay(subject="测试超市", out_trade_no=out_trade_no, total_amount=str(money))
    print(out_trade_no)
    print()
    # 获取扫码支付的请求地址
    url = alipay.gateway+"?"+params
    print(url)
    return HttpResponseRedirect(url)


# 校验是否支付完成
def checkpay_view(request):
    if request.method == "GET":
        #获取所有请求参数
        params = request.GET.dict()
        print("--------:{}".format(params))
        #移除并获取sign参数的值
        sign = params.pop('sign')

        #校验是否支付成功
        if alipay.verify(params,sign):
            return HttpResponse('同步支付成功！')
        return HttpResponse('同步支付失败！')
    if request.method == "POST":
        # 获取所有请求参数
        params = request.data.dict()
        print("--------:{}".format(params))
        # 移除并获取sign参数的值
        sign = params.pop('sign')

        # 校验是否支付成功
        if alipay.verify(params, sign):
            return HttpResponse('异步支付成功！')
        return HttpResponse('异步支付失败！')
