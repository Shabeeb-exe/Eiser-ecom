from django.db import models
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import JSONField

# Create your models here.
    
class Login(models.Model):
    emailorphone = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    salt = models.CharField(max_length=255)
    type = models.CharField(max_length=30)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)
    otp_cooldown = models.DateTimeField(null=True, blank=True)  # Cooldown period for resending OTP

    class Meta:
        verbose_name = "Login"
        verbose_name_plural = "Logins"
        ordering = ["emailorphone"]

    def __str__(self):
        return f"{self.emailorphone}"

class Signup(models.Model):
    name=models.CharField(max_length=50)
    emailorphone=models.CharField(max_length=100)
    photo=models.FileField(upload_to='user_photos/', null=True, blank=True)
    place=models.CharField(max_length=100)
    pincode=models.IntegerField()
    state=models.CharField(max_length=50)
    gender=models.CharField(max_length=10) 
    date=models.DateTimeField(default=now)
    login=models.ForeignKey(Login,on_delete=models.CASCADE)


    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ["-date"]

    def __str__(self):
        return f"{self.date}"
    
class Seller(models.Model):
    name=models.CharField(max_length=50)
    emailorphone=models.CharField(max_length=100)
    photo=models.FileField(upload_to='user_photos/', null=True, blank=True)
    place=models.CharField(max_length=100)
    pincode=models.IntegerField()
    state=models.CharField(max_length=50)
    gender=models.CharField(max_length=10) 
    date=models.DateTimeField(default=now)
    license = models.FileField(upload_to='business_licenses/')  # Business proof
    id_proof = models.FileField(upload_to='id_proofs/')  # Id proof
    login=models.ForeignKey(Login,on_delete=models.CASCADE)


    class Meta:
        verbose_name = "Seller"
        verbose_name_plural = "Sellers"
        ordering = ["-date"]

    def __str__(self):
        return f"{self.date}"

class Category(models.Model):
    name=models.CharField(max_length=50)
    thumbnail=models.FileField(upload_to='category_thumbs/')

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"
    
class SubCategory(models.Model):
    name=models.CharField(max_length=50)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    thumbnail=models.FileField(upload_to='subcategory_thumbs/')

    class Meta:
        verbose_name = "Sub category"
        verbose_name_plural = "Sub categories"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name=models.CharField(max_length=200)
    brand=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    desc=models.CharField(max_length=1000)
    thumbnail=models.FileField(upload_to='product_imgs/')
    images = models.ManyToManyField('ProductImg')
    videos = models.ManyToManyField('ProductVid', blank=True)
    subcategory=models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    seller=models.ForeignKey(Seller,on_delete=models.CASCADE)
    instock=models.IntegerField()

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"

class ProductImg(models.Model):
    image=models.FileField(upload_to='product_imgs/')
    
class ProductVid(models.Model):
    video=models.FileField(upload_to='product_vids/')

class Coupon(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    coupon=models.CharField(max_length=50,null=True, blank=True)
    cdiscount=models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)

class AppliedCoupon(models.Model):
    user = models.ForeignKey('Signup', on_delete=models.CASCADE)
    coupon = models.ForeignKey('Coupon', on_delete=models.CASCADE)
    applied_date = models.DateField(default=now)
    status = models.CharField(
        max_length=20,
        choices=[('NotApplied', 'NotApplied'), ('Applied', 'Applied'), ('Used', 'Used')],
        default='NotApplied'
    )
  

class Offer(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    discount=models.DecimalField(max_digits=5, decimal_places=2)
    sdate=models.DateField(default=now)
    edate=models.DateField(default=now)

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('Signup', on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    comment = models.TextField()
    pdate = models.DateTimeField(default=now)
    
    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ["-pdate"]

    def __str__(self):
        return f"Review by {self.user.name} on {self.product.name}"

class Wishlist(models.Model):
    user = models.ForeignKey('Signup', on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    date = models.DateField(default=now)

class Cart(models.Model):
    user = models.ForeignKey('Signup', on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    offer = models.ForeignKey('Offer', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(default=now)
    offer_amount=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    coupon_amount=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Submitted', 'Submitted')],
        default='Pending'
    )

      
class Checkout(models.Model):
    user = models.ForeignKey('Signup', on_delete=models.CASCADE)
    cart_data = JSONField(null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=now)
    payment_status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Initiated', 'Initiated'), ('Completed', 'Completed')],
        default='Pending'
    )
    delivery_status=models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'),
        ('Dispatched', 'Dispatched'),
        ('In Transit', 'In Transit'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled') ],
        default='Pending'
    )
    delivered_at = models.DateTimeField(null=True, blank=True) #for returning item purposes

class OrderItem(models.Model):    
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at the time of purchase

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        ordering = ["-checkout"]

    def __str__(self):
        return f"{self.checkout}"

class DeliveryDetails(models.Model):
    checkout = models.ForeignKey('Checkout', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    state = models.CharField(max_length=100)
    pincode = models.PositiveIntegerField()
    notes = models.CharField(max_length=2000, null=True, blank=True)
    payment_method = models.CharField(max_length=50)

class Payment(models.Model):
    checkout=models.ForeignKey('Checkout',on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    date=models.DateTimeField(default=now)

class ReturnedItems(models.Model):
    order = models.ForeignKey('OrderItem', on_delete=models.CASCADE)
    delivery = models.ForeignKey('DeliveryDetails', on_delete=models.CASCADE)
    date = models.DateTimeField(default=now)
    status = models.CharField(
        max_length=50,
        choices=[('Return Pending', 'Return Pending'),
        ('Returned Item Picked Up', 'Returned Item Picked Up'),
        ('Item Returned', 'Item Returned'), ],
        default='Return Pending'
    )

class DeliveryFeedback(models.Model):
    order = models.ForeignKey('OrderItem', on_delete=models.CASCADE)
    user = models.ForeignKey('Signup', on_delete=models.CASCADE)
    feedback = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    date = models.DateTimeField(default=now) 

class Complaint(models.Model):
    user = models.ForeignKey('Signup', on_delete=models.CASCADE)
    date = models.DateTimeField(default=now) 
    order = models.ForeignKey('OrderItem', on_delete=models.CASCADE)
    complaint = models.TextField()  

class DeliveryBoy(models.Model):
    name=models.CharField(max_length=50)
    emailorphone=models.CharField(max_length=100)
    photo=models.FileField(upload_to='dboy_photos/', null=True, blank=True)
    place=models.CharField(max_length=100)
    pincode=models.IntegerField()
    state=models.CharField(max_length=50)
    gender=models.CharField(max_length=10) 
    date=models.DateTimeField(default=now)
    id_proof = models.FileField(upload_to='delivery_boy_ids/')  # Id proof
    login=models.ForeignKey(Login,on_delete=models.CASCADE) 

    class Meta:
        verbose_name = "Delivery Boy"
        verbose_name_plural = "Delivery Boys"
        ordering = ["-date"]

    def __str__(self):
        return f"{self.name}"

class OrderAssignDeliveryBoy(models.Model):
    order = models.ForeignKey('OrderItem', on_delete=models.CASCADE)
    dboy = models.ForeignKey('DeliveryBoy', on_delete=models.CASCADE)
    date = models.DateTimeField(default=now)

class Contact(models.Model):
    login = models.ForeignKey('Login',on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    date = models.DateTimeField(default=now)

    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ["-date"]

    def __str__(self):
        return f"{self.date}"
    
class SearchHistory(models.Model):
    user = models.ForeignKey('Signup', on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} searched for {self.query} at {self.searched_at}"