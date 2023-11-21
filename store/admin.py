from django.contrib import admin
from .models import Category,Product,Cart,OrderPlaced,Customer,Payment

# Register your models here.

admin.site.register(Category)
# admin.site.register(Product)

@admin.register(Cart)
class CardModelAdmin(admin.ModelAdmin):
  list_display=['user','product','product_qty']
  
@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
  list_display=['id','user','customer','product','quantity','order_date','status','payment']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
  list_display =['id','user','name','localty','city','zipcode','state']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
  list_display=['name','selling_price','orginal_price','description','category','product_image','quntity']

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
  list_display=['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']
