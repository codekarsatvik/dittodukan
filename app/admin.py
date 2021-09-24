from django.contrib import admin
from app.models import Product,Customer,Cart,OrderPlaced
# Register your models here.
#  here we have to register our models 

class ProductAdminModal(admin.ModelAdmin):
    list_display = ['id','title','discounted_price','description','product_image']
admin.site.register(Product,ProductAdminModal)

class CustomerAdminModal(admin.ModelAdmin):
    list_display = ['id','name','city','pincode','state']
admin.site.register(Customer,CustomerAdminModal)

class CartAdminModal(admin.ModelAdmin):
    list_display = ['id','product','user']
admin.site.register(Cart,CartAdminModal)

class OrderPlacedAdminModal(admin.ModelAdmin):
    list_display = ['id','user','ordered_date','product','quantity']
admin.site.register(OrderPlaced,OrderPlacedAdminModal)