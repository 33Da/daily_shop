from django.shortcuts import render
from df_goods.models import TypeInfo,GoodInfo
from django.core.paginator import Paginator

# Create your views here.
def index(request):

    cart_count=get_cartcount(request)


    # 查询各分类最热的四条数据，最新的四条
    # 先获取到所有分类
    typelist=TypeInfo.objects.all()

    # 第一个分类:最新的四条（id）
    type0_new=typelist[0].goodinfo_set.order_by('-id')[0:4]
    # 第一个分类: 点击最高的四条（gclick）
    type0_click=typelist[0].goodinfo_set.order_by('-gclick')[0:4]

    # 第二个分类:最新的四条（id）
    type1_new = typelist[1].goodinfo_set.order_by('-id')[0:4]
    # 第二个分类: 点击最高的四条（gclick）
    type1_click = typelist[1].goodinfo_set.order_by('-gclick')[0:4]

    # 第三个分类:最新的四条（id）
    type2_new = typelist[2].goodinfo_set.order_by('-id')[0:4]
    # 第三个分类: 点击最高的四条（gclick）
    type2_click = typelist[2].goodinfo_set.order_by('-gclick')[0:4]

    # 第四个分类:最新的四条（id）
    type3_new = typelist[3].goodinfo_set.order_by('-id')[0:4]
    # 第四个分类: 点击最高的四条（gclick）
    type3_click = typelist[3].goodinfo_set.order_by('-gclick')[0:4]

    # 第五个分类:最新的四条（id）
    type4_new = typelist[4].goodinfo_set.order_by('-id')[0:4]
    # 第五个分类: 点击最高的四条（gclick）
    type4_click = typelist[4].goodinfo_set.order_by('-gclick')[0:4]

    # 第六个分类:最新的四条（id）
    type5_new = typelist[5].goodinfo_set.order_by('-id')[0:4]
    # 第六个分类: 点击最高的四条（gclick）
    type5_click = typelist[5].goodinfo_set.order_by('-gclick')[0:4]

    context = {
        "username": " ",
        "title": "首页",
        'type0_new':type0_new,'type0_click':type0_click,
        'type1_new':type1_new,'type1_click':type1_click,
        'type2_new': type2_new, 'type2_click': type2_click,
        'type4_new': type4_new, 'type4_click': type4_click,
        'type3_new':type3_new,'type3_click':type3_click,
        'type5_new': type5_new, 'type5_click': type5_click,
        'cart_count':cart_count,

    }

    # 用get方法获取session，若不存在则设置None值（第二个参数）
    username = request.session.get("user_name", None)
    if username is not None:
        context["username"] = username

    return render(request,'df_goods/index.html',context)






def detail(request,good_id):
    username=get_user(request)
    good=GoodInfo.objects.get(pk=good_id)
    good.gclick=good.gclick+1
    good.save()
    new=good.gtype.goodinfo_set.order_by('-id')[0:2]

    cart_count=get_cartcount(request)

    context={
        'news':new,
        'title':good.gtype.ttitle,
        'g':good,
        'guest_cart':0,
        'good_id':good_id,
        'username':username,
        'cart_count':cart_count,

    }
    response=render(request,'df_goods/detail.html',context)
    #记录最近浏览
    goods_ids=request.COOKIES.get('goods_ids','')
    goods_id='%d'%good.id
    if goods_ids!='':
        goods_ids1=goods_ids.split(',')
        if goods_ids1.count(goods_id)>=1:
            goods_ids1.remove(goods_id)
        goods_ids1.insert(0,goods_id)  #添加到第一个
        if len(goods_ids1)>=6:  #如果超过六个
            del goods_ids1[5]
        goods_ids=','.join(goods_ids1)
    else:
        goods_ids=goods_id #没有浏览记录直接加
    response.set_cookie('goods_ids',goods_ids)  #写入cookier
    return response

def list(request,type_id,pindex,sort):
    username=get_user(request)

    cart_count=get_cartcount(request)
    # 由type_id获取到分类
    typeinfo=TypeInfo.objects.get(pk=int(type_id))
    # 设置新品推荐
    news=typeinfo.goodinfo_set.order_by('-id')[0:2]
    if sort==1:  #默认排序
        goods_list=GoodInfo.objects.filter(gtype=type_id).order_by('-id')
    elif sort==2: #价格
        goods_list=GoodInfo.objects.filter(gtype=type_id).order_by('-gprice')

    elif sort==3: #人气
        goods_list=GoodInfo.objects.filter(gtype=type_id).order_by('-gclick')

    # 分页，每页10个
    paginator=Paginator(goods_list,10)
    # 当前页面
    page=paginator.page(pindex)


    context={
        'title':typeinfo.ttitle,
        'page':page,
        'paginator':paginator,
        'typeinfo':typeinfo,
        'sort':sort,
        'news':news,
        'guest_cart': 0,
        'username':username,
        'cart_count':cart_count,

    }
    return render(request,'df_goods/list.html',context)

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

# 自定义搜索视图类
from haystack.views import SearchView
class MySerchView(SearchView):
    # 定义上下文
    def extra_context(self):
        context=super(MySerchView,self).extra_context()
        username=get_user(self.request)
        cart_count=get_cartcount(self.request)
        context['title']='搜索'
        context['cart_count']=cart_count
        context['username']=username
        return context
