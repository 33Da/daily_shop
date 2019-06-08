import re
from datetime import datetime
from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import render, redirect
from freshfruit import user_decorator
from django.db import transaction
from df_order.models import *
from df_cart.models import *
from freshfruit.models import *


# Create your views here.

@user_decorator.login_check
def order(request):
    username=get_user(request)
    cart_count=get_cartcount(request)
    cart_ids=request.GET.getlist('cart_ids')
    carts=[]
    for cart_id in cart_ids:
        cart=CartInfo.objects.get(pk=int(cart_id))
        carts.append(cart)

    user=Userinfo.objects.filter(usename=username).first()



    context={
        'title':'提交订单',
        'username':username,
        'cart_count':cart_count,
        'carts':carts,
        'user':user
    }
    return render(request,'df_order/place_order.html',context)


"""
事务：一旦操作失败则回滚  @transaction.atomic()
1、创建订单
2、判断商品库存
3、创建商品详细对象
4、修改商品库存
5、删除购物车

"""
@transaction.atomic()
@user_decorator.login_check
def order_handle(request):
    # 设置回滚点
    tran_id=transaction.savepoint()
    #接受购物车编号
    if request.is_ajax():
        if request.method=='POST':
            cart_ids = request.POST.getlist('cart_ids')
            total = request.POST.get('total')
            # 取数值部分
            total=re.sub("\D", "", total)

            try:
                # 创建订单对象
                order = OrderInfo()
                now = datetime.now()
                uid = request.session['user_id']
                order.oid = '%s%d' % (now.strftime('%Y%m%d%H%H%S'), uid)
                order.user_id = uid
                order.odata = now
                order.ototal = Decimal(int(total))
                order.save()

                # 创建详细对象
                # cart_ids1 = [int(item) for item in cart_id.split(',')]
                for id1 in cart_ids:
                    detail = OrderDetailInfo()
                    detail.order = order
                    cart = CartInfo.objects.get(id=id1)
                    # 判断商品库存
                    goods = cart.goods
                    if goods.gkucun >= cart.count:
                        goods.gkucun = goods.gkucun - cart.count
                        goods.save()
                        # 完善详细信息
                        detail.goods_id = goods.id
                        detail.price = goods.gprice
                        detail.count = cart.count
                        detail.save()
                        # 删除购物车数据
                        cart.delete()
                        request.session['cart_count'] = 0
                        data={'res': 5}
                    else:
                        # 超过库存就回滚
                        transaction.savepoint_rollback(tran_id)
                        data={"msg": "超过库存"}
                transaction.savepoint_commit(tran_id)
                return JsonResponse(data)
            except Exception as e:
                print("-------------------------------------{0}".format(e))
                # 回滚
                transaction.savepoint_rollback(tran_id)
                data={'msg': "失败"}




# 获取登录名
def get_user(request):
    username = request.session.get("user_name", None)
    if username is not None:
        return username
    else:
        return None

#获取购物车数量
def get_cartcount(request):
    count=request.session.get("cart_count",None)
    if count is not None:
        return count
    else:
        return 0
