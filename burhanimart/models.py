from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class SliderBanner(models.Model):
    banner_image_1 = models.ImageField(upload_to="banner_image")
    banner_image_2 = models.ImageField(upload_to="banner_image")
    banner_image_3 = models.ImageField(upload_to="banner_image")
    banner_image_4 = models.ImageField(upload_to="banner_image")
    banner_image_5 = models.ImageField(upload_to="banner_image")
 
# GENDER = (
#     ('Male','Male'),
#     ('Female','Female'),
#     ('Other','Other')
# )

# class PersonalInformation(models.Model):
#     user = models.ForeignKey(User , on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     mobile_number = models.IntegerField()
#     gender = models.CharField(max_length=20 , choices=GENDER)

class ContactUs(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=50)
    customer_email = models.EmailField(max_length=100)
    mobile_number = models.IntegerField()
    query = models.TextField(max_length=500)
    query_date = models.DateTimeField(auto_now_add=True)

CATEGORY_CHOICE=(
    ('cloth','cloth'),
    ('emitation_jewellery', 'emitation_jewellery'),
    ('topi','topi'),
    ('rida','rida')
)

SUB_CATEGORY_CHOICE = (
    ('rida','rida'),
    ('kurta_izar','kurta_izar'),
    ('night_dress', 'night_dress')
)

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_image_1 = models.ImageField(upload_to="product_images")
    product_image_2 = models.ImageField(upload_to="product_images")
    product_image_3 = models.ImageField(upload_to="product_images")
    product_image_4 = models.ImageField(upload_to="product_images")
    product_image_5 = models.ImageField(upload_to="product_images")
    product_selling_price = models.IntegerField()
    product_discounted_price = models.IntegerField()
    product_description = models.TextField(max_length=1000)
    product_suitable_for = models.CharField(max_length=200)
    product_brand = models.CharField(max_length=50)
    product_seller = models.CharField(max_length=50)
    product_category = models.CharField(max_length=20 , choices=CATEGORY_CHOICE)
    product_sub_category = models.CharField(max_length=20, choices=SUB_CATEGORY_CHOICE)
    product_upload_date = models.DateTimeField(auto_now_add=True)


    @property
    def discount_percentage(self):
        return round(100 * (self.product_selling_price - self.product_discounted_price) / self.product_selling_price)

    @property
    def save_price(self):
        return self.product_selling_price - self.product_discounted_price

class CustomerAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    customer_name = models.CharField(max_length=50)
    mobile_number = models.IntegerField()
    area_locality = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.IntegerField()

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def discount_percentage(self):
        return round(100 * (self.product.product_selling_price - self.product.product_discounted_price) / self.product.product_selling_price)
    @property
    def total_cost(self):
        return self.quantity * self.product.product_discounted_price
    @property
    def save_price(self):
        return self.product.product_selling_price - self.product.product_discounted_price
    

ORDER_STATUS =(
    ('Order Confirm', 'Order Confirm'),
    ('Packed','Packed'),
    ('Shipped','Shipped'),
    ('Out of Delivery','Out of Delivery'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)


class Payment(models.Model):
    amount = models.FloatField()
    currency = models.CharField(max_length=3, null=True)
    order_id = models.CharField(max_length=32, null=True)
    receipt = models.CharField(max_length=32, null=True)
    payment_capture = models.IntegerField(default=0, null=True)
    payment_id = models.CharField(max_length=64, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    address = models.ForeignKey(CustomerAddress , on_delete=models.CASCADE)
    # payment = models.ForeignKey(Payment , on_delete=models.CASCADE, default="",null=True)
    # amount = models.FloatField()
    amount = models.PositiveBigIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    total_amount = models.PositiveIntegerField(default=0)
    order_placed_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(choices=ORDER_STATUS , max_length=20 ,default="Order Confirm")
    currency = models.CharField(max_length=3, default="")
    order_id = models.CharField(max_length=32, default="")
    receipt = models.CharField(max_length=32, default="")
    payment_capture = models.IntegerField(default=0)
    # payment_id = models.CharField(max_length=64,default="")
    # created_at = models.DateTimeField(auto_now_add=True, default="")
    # updated_at = models.DateTimeField(auto_now=True, default="")

    @property
    def total_cost(self):
        return self.quantity * self.product.product_discounted_price

    @property
    def discounted_price(self):
        return self.product.product_discounted_price



