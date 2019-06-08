from django.http import JsonResponse
from django.shortcuts import render, redirect
from freshfruit import user_decorator
from df_cart.models import *
from df_goods.models import *
from freshfruit.models import *

# Create your views here.
@user_decorator.login_check
def cart(request):
    username=get_user(request)
    uid=request.session['user_id']
    carts=CartInfo.objects.filter(user=uid)
    count=carts.count()


    context={
        'title':'购物车',
        'username':username,
        'carts':carts,
        'count':count,

    }
    return render(request,'df_cart/cart.html',context)


# 添加商品
@user_decorator.login_check
def add(request,gid,count):
    # gid:物品id   count:数量
    uid=request.session['user_id']
    gid=gid
    count=count
    user=Userinfo.objects.get(pk=uid)
    good=GoodInfo.objects.get(pk=gid)
    # 查询数据库看有没有这个订单信息
    carts=CartInfo.objects.filter(user=uid,goods=gid)

    if len(carts)>=1:  #如果有这条信息
        cart=carts[0]
        cart.count=cart.count+count
    else:  #没有就添加这条信息
        cart=CartInfo()
        cart.user=user
        cart.goods=good
        cart.count=count
        request.session['cart_count'] +=1
    cart.save()

    """
    有两种情况,
    1:在列表页面点击加入购物车是直接进入到购物车页面的
    2:在商品详细页面则是通过ajax的方式加入到购物车的,这时页面不用跳到购物车页面,只要返回数量
    """
    if request.is_ajax(): #如果是ajax提交的就返回json数据
        count=CartInfo.objects.filter(user=request.session['user_id']).count()
        return JsonResponse({'count':count})
    else:
        return redirect('/cart/')

#修改商品
@user_decorator.login_check
def edit(request,cart_id,count):
    try:
        cart=CartInfo.objects.get(pk=cart_id)
        count1=cart.count=count
        cart.save()
        data={'ok':0}
    except Exception as e:
        data={'ok':count1}
    return JsonResponse(data)


# 删除
@user_decorator.login_check
def delete(request,cart_id):
    try:
        cart=CartInfo.objects.get(pk=cart_id)
        cart.delete()
        request.session['cart_count'] -= 1
        data={'ok':1}
    except Exception as e:
        data={'ok':0}
    return JsonResponse(data)







# 获取登录名
def get_user(request):
    username = request.session.get("user_name", None)
    if username is not None:
        return username
    else:
        return None