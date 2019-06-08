from django.db import models

# Create your models here.
class Userinfo(models.Model):
    usename=models.CharField(max_length=20)
    userpwd=models.CharField(max_length=80)
    useremail=models.CharField(max_length=30)
    usretel=models.CharField(max_length=11,default='')
    useraddress=models.CharField(max_length=100,default='')
    # 邮编
    youbian=models.CharField(max_length=6,default='')
    # 收件人
    usershow=models.CharField(max_length=20,default='')