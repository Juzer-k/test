from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import SliderBanner , ContactUs , Product,CustomerAddress, Cart, OrderPlaced
# Register your models here.

@admin.register(SliderBanner)
class SliderModelAdmin(admin.ModelAdmin):
    list_display =['id','banner_image_1','banner_image_2','banner_image_3','banner_image_4','banner_image_5']

@admin.register(ContactUs)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'customer_name','customer_email','mobile_number','query','query_date')

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','product_name','product_selling_price','product_discounted_price','product_brand','product_seller','product_upload_date']

@admin.register(CustomerAddress)
class CustomerAddressModelAdmin(admin.ModelAdmin):
    list_display=['id','user','customer_name','mobile_number','area_locality','city','state','zip_code']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product_info','quantity']

    def product_info(self, obj):
        link= reverse("admin:burhanimart_product_change",args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.product_name)

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product_info','address_info','amount','quantity','total_amount','order_placed_date','order_status']

    # def user_info(self, obj):
    #     link= reverse("admin:burhanimart_user_change",args=[obj.user.pk])
    #     return format_html('<a href="{}">{}</a>', link, obj.user.fname)

    def product_info(self, obj):
        link= reverse("admin:burhanimart_product_change",args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.product_name)

    def address_info(self, obj):
        link= reverse("admin:burhanimart_customeraddress_change",args=[obj.address.pk])
        return format_html('<a href="{}">{}</a>', link, obj.address.customer_name)