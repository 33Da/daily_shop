from django.db import models

# Create your models here.
class CartInfo(models.Model):
    user=models.ForeignKey('freshfruit.Userinfo',on_delete='"CASCADE"')
    goods=models.ForeignKey('df_goods.GoodInfo',on_delete="CASCADE")
    # 买了几个
    count=models.IntegerField()