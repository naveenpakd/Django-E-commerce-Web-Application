from django.db import models
from django.contrib.auth.models import  User

# Create your models here.

STATE_CHOISES=(
  ('Kerala ','Kerala'),
  ('Karnadaka ','Karnadaka'),
  ('Thamizhnadu','Thamizhnadu'),
  ('Goa','Goa')
  )

class Category(models.Model):
    slug=models.CharField(max_length=60,null=False,blank=False)
    name=models.CharField(max_length=200,null=False,blank=False)
    image=models.ImageField(upload_to="imagess",null=False,blank=False)
    status=models.BooleanField(default=False, help_text="0=default,1=Hidden")
    trending=models.BooleanField(default=False, help_text="0=default,1=Hidden")
    def __str__(self):
        return self.name
    
class Product(models.Model):
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    slug=models.CharField(max_length=180, null=False, blank=False)
    name=models.CharField(max_length=180, null=False, blank=False)
    product_image=models.ImageField(upload_to="imagess", null=False, blank=False)
    description=models.CharField(max_length=1000, null=False, blank=False)
    quntity=models.IntegerField(null=False, blank=False)
    orginal_price=models.FloatField(null=False, blank=False)
    selling_price=models.FloatField(null=False, blank=False)
    status=models.BooleanField(default=False,help_text="0=default, 1=Hidden")
    trending=models.BooleanField(default=False,help_text="0=default,1=Trending")
    def __str__(self):
        return self.name
    

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE) 
    product =models.ForeignKey(Product,on_delete=models.CASCADE)
    product_qty=models.IntegerField(null=False,blank=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
     return str(self.id)
    
    @property
    def total_cost(self):
        return self.product_qty * self.product.selling_price    


class Customer(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer')
  name = models.CharField(max_length=200)
  localty = models.CharField(max_length=200)
  city = models.CharField(max_length=50)
  mobile = models.BigIntegerField(default=0)
  zipcode = models.IntegerField()
  state = models.CharField(choices=STATE_CHOISES,max_length=40)
  
  def __str__(self):
    return str(self.id)     
    

STATUS_CHOISES=(
  ('Accepted','Accepted'),
  ('Packed','Packed'),
  ('On The Way','On The Way'),
  ('Delivered','Delivered'),
  ('Cancel','Cancel'),
  ('Pending','Pending'),
  )
  

class Payment(models.Model):
   user = models.ForeignKey(User,on_delete=models.CASCADE)
   amount = models.FloatField()
   razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
   razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
   razorpay_payment_id =  models.CharField(max_length=100,blank=True,null=True)
   paid = models.BooleanField(default=False)



  
class OrderPlaced(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField(default=1)
  order_date=models.DateTimeField(auto_now_add=True)
  status =models.CharField(choices=STATUS_CHOISES,max_length=50,default='Pending')
  payment = models.ForeignKey(Payment,on_delete=models.CASCADE,default="")
  
  @property
  def total_cost(self):
    return self.quantity * self.product.selling_price
  
  # def __str__(self):
  #       return self.payment
  
        
