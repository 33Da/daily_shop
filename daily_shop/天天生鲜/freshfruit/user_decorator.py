from django.http import HttpResponseRedirect
#如果未登录可转向登陆页
def login_check(func):
    def login_fun(request,*args,**kwargs):
        if request.session.has_key('user_name'):
            return func(request,*args,**kwargs)
        else:
            red=HttpResponseRedirect('/user/login')
            # 把上一次浏览的页面保存到cookier
            red.set_cookie('url',request.get_full_path())
            return red
    return login_fun


"""
http://127.0.0.1:8080/200/?type=10
request.path:表示当前路径，/200/
request.get_full_path（）：表示取得完整路径，/200/?type=10




"""