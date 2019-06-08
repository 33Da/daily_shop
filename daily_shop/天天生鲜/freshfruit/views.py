from django.contrib.auth.hashers import make_password,check_password
from django.http import JsonResponse
from django.shortcuts import render,redirect,HttpResponseRedirect
from .models import *
from . import user_decorator
from df_goods.models import GoodInfo
from df_cart.models import CartInfo
from df_order.models import *
from django.core.paginator import Paginator
# Create your views here.
def register(request):
    context={'title':'用户注册'}
    return render(request,'df_user/register.html',context)

def register_handle(request):
    if request.method=='POST':
        post=request.POST
        username=post.get('user_name')
        pwd=post.get('pwd')
        pwd2=post.get('cpwd')
        email=post.get('email')

        if pwd==pwd2:
            # 加密
            sh1_pwd = make_password(pwd)
            user=Userinfo(usename=username,userpwd=sh1_pwd,useremail=email)
            user.save()
            return redirect('login/')
        else:
            return redirect('register/')

def login(request):
    # 看有没有记住用户，有取出uname，没有就为''（空）
    username=request.COOKIES.get('uname','')
    context={'title':'用户登录','error_name':0,'error_pwd':0,'username':username}
    return render(request,'df_user/login.html',context)

def login_handle(requset):
    post=requset.POST
    username=post.get('username')
    password=post.get('pwd')
    jizhu=post.get('jizhu',0)

    users=Userinfo.objects.filter(usename=username)

    if len(users)==1:
        if check_password(password, users[0].userpwd):
            # 存在seesion中

            # 获取到登陆前在哪个页面上，如果没有则登陆后取首页
            url=requset.COOKIES.get('url','/')
            response = HttpResponseRedirect(url)

            # 记住用户
            if jizhu != 0:
                # 写cookier

                response.set_cookie('user_id',users[0].id)
            else:
                # set_cookie:第一个参数是
                response.set_cookie('uname', '', max_age=-1)


            requset.session['user_name']=username
            requset.session['user_id']=users[0].id

            count=CartInfo.objects.filter(user=users[0].id).count()
            requset.session['cart_count']=count
            return response
        # 密码不对
        else:
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': username, 'upwd': password}
            return render(requset, 'df_user/login.html', context)
    # 没有该用户
    else:
        context={'titile':'用户登录','error_name':1,'error_pwd':0,'uname':username,'upwd':password}
        return render(requset,'df_user/login.html',context)


# 登出
def logout(request):
    request.session.flush()#清空当前用户所有session
    return redirect('/')





@user_decorator.login_check
def user_site(request):
    username = get_user(request)
    users=Userinfo.objects.filter(usename=username).first()
    if request.method=='POST':
        post = request.POST
        usershow = post.get('usershow')
        useraddress = post.get('useraddress')
        youbian = post.get('youbian')
        tel = post.get('tel')

        users.useraddress=useraddress
        users.usretel=tel
        users.usershow=usershow
        users.youbian=youbian
        users.save()




    context={
        'address':users.useraddress,
        'telphone':users.usretel,
        'usershow':users.usershow,
        'youbian':users.youbian,
        'username':users.usename,
        'title':"用户中心"
    }
    return render(request,'df_user/user_center_site.html',context=context)




# 没登陆跳到这个界面
@user_decorator.login_check
def info(request):
    uname=request.session.get('user_name')
    user=Userinfo.objects.filter(usename=uname).first()
    #显示最近浏览
    goods_ids=request.COOKIES.get('goods_ids','')
    goods_list = []
    if goods_ids != '':
        goods_ids1 = goods_ids.split(',')

        for goods_id in goods_ids1:
            goods_list.append(GoodInfo.objects.get(id=int(goods_id)))



    context={'title':'用户中心','username':uname,'address':user.useremail,'goods_list':goods_list,}
    return render(request,'df_user/user_center_info.html',context)

def register_username(request):
    uname=request.POST.get('username')
    if len(Userinfo.objects.filter(usename=uname)) == 0:
        return JsonResponse({'error':0})
    else:
        return JsonResponse({'error':1})

@user_decorator.login_check
def order(request,pindex):
    username=get_user(request)
    user_id=request.session['user_id']
    order_list=OrderInfo.objects.filter(user=user_id).order_by('-oid')
    goods_list=[]

    for order in order_list:

        order1=order.orderdetailinfo_set.all()
        order_dict = {
            'order': order,
            'good_list': order1,

        }
        goods_list.append(order_dict)


    # 分页，每页5个
    paginator = Paginator(goods_list,4)
    # 当前页面
    page = paginator.page(pindex)

    """
    page代替了goods_list,传给模板时只要传page就是传goods_list
    """


    context={
        'username':username,
        'page': page,
        'title': '个人订单'

    }
    return render(request,'df_user/user_center_order.html',context)

# 获取登录名
def get_user(request):
    username = request.session.get("user_name", None)
    if username is not None:
        return username
    else:
        return None


