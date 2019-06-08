from django.db import models

# Create your models here.

# 订单类
class OrderInfo(models.Model):
    # 订单编号
    oid=models.CharField(max_length=20,primary_key=True)
    #购买者
    user=models.ForeignKey('freshfruit.Userinfo',on_delete='"CASCADE"')
    #购买日期
    odata=models.DateTimeField(auto_now=True)
    #是否付款
    oIspay=models.BooleanField(default=False)
    #总金额
    ototal=models.CharField(max_length=150)


#清单详细
class OrderDetailInfo(models.Model):
    goods=models.ForeignKey('df_goods.GoodInfo',on_delete="CASCADE")
    order=models.ForeignKey(OrderInfo,on_delete="CASCADE")
    price=models.DecimalField(max_digits=5,decimal_places=2)
    count=models.IntegerField()
