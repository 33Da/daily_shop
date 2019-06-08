from django.db import models
from tinymce.models import HTMLField


# Create your models here.

# 类型类
class TypeInfo(models.Model):
    # 水果类型名
    ttitle=models.CharField(max_length=20)
    # 删除键
    isDelete=models.BooleanField(default=False)
    def __str__(self):
        return self.ttitle


# 商品
class GoodInfo(models.Model):

    # 商品名
    gtitle=models.CharField(max_length=20)
    #图片  upload_to:上传文件
    gpic=models.ImageField(upload_to="df_goods")
    # 价格
    gprice=models.DecimalField(max_digits=5,decimal_places=2)
    # 删除键
    isDelete=models.BooleanField(default=False)
    # 单位
    gunit=models.CharField(max_length=20,default='500g')
    # 点击量
    gclick=models.IntegerField()
    # 简介
    gjianjie=models.CharField(max_length=200)
    # 库存
    gkucun=models.IntegerField()
    # 详细介绍
    gcontent=HTMLField()
    # 分类
    gtype=models.ForeignKey(TypeInfo,on_delete="CASCADE")

    def __str__(self):
        return self.gtitle
