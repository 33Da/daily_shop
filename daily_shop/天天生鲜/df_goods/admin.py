from django.contrib import admin
from df_goods.models import *

# Register your models here.
class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id','ttitle']


class GoodsInfoAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ['id',"gtitle",'gunit','gkucun','gclick','gpic','gprice','gcontent','gjianjie','gtype']


admin.site.register(TypeInfo,TypeInfoAdmin)
admin.site.register(GoodInfo,GoodsInfoAdmin)
