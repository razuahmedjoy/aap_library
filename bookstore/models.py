from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
import os
from PIL import Image
from django.conf import settings
import uuid
from ckeditor.fields import RichTextField

from . import send_tele


# Create your models here.


class Main_Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, allow_unicode=True, unique=True)
    position = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ('position', )

    def __str__(self):
        return self.name


class Sub_Category(models.Model):
    parent_category = models.ForeignKey(
        Main_Category, null=True, blank=True, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, allow_unicode=True, unique=True)

    def __str__(self):
        return self.name


# model for author
class Author(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=255, allow_unicode=True, unique=True)
    details = models.TextField(null=True, blank=True)
    photo = models.ImageField(null=True, blank=True, upload_to='authors')


    def __str__(self):
        return self.name


# model for publisher
class Publisher(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=255, allow_unicode=True, unique=True)
    details = models.TextField(null=True, blank=True)
    photo = models.ImageField(null=True, blank=True, upload_to='publishers')

    def __str__(self):
        return self.name


class Books(models.Model):
    def book_cover_photo(instance, filename):
        ext = filename.split(".")[-1]
        filename = "%s.%s" % (instance.title, ext)

        full_path = os.path.join(settings.MEDIA_ROOT, filename)
        if os.path.exists(full_path):
            os.remove(full_path)
        return os.path.join("books/", filename)

    title = models.CharField(max_length=250, blank=True, null=True)

    # changed author and publisher to foreignkey
    author = models.ForeignKey(
        Author, on_delete=models.PROTECT, null=True, related_name="books", blank=True
    )
    publisher = models.ForeignKey(
        Publisher, on_delete=models.PROTECT, null=True, related_name="books", blank=True
    )

    mrp_price = models.CharField(max_length=20, blank=True, null=True)

    cover_photo = models.ImageField(null=True, blank=True, upload_to=book_cover_photo)
    price = models.IntegerField(null=True, blank=True)
    category = models.ManyToManyField(Sub_Category, blank=True)
    slug = models.SlugField(max_length=255, allow_unicode=True)
    in_stock = models.BooleanField(default=True)
    description = RichTextField(null=True, blank=True)
    book_id = models.UUIDField(default=uuid.uuid4, unique=True)
    pdf = models.FileField(null=True, blank=True, upload_to="books/pdf/")
    created_at = models.DateTimeField(auto_now_add=True)
    exchangeable = models.BooleanField(default=False)
    exchangeable_stock = models.IntegerField(blank=True, null=True)
    exchange_value = models.IntegerField(default=1, null=True, blank=True)
    serial_number = models.IntegerField(null=True, blank=True)
    preparation = models.CharField(max_length=260,null=True, blank=True)

    def __str__(self):
        return self.title

    
    class Meta:
        ordering = ('serial_number', )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        SIZE = 180, 280

        if self.cover_photo:
            pic = Image.open(self.cover_photo.path)
            pic.thumbnail(SIZE, Image.LANCZOS)
            pic.save(self.cover_photo.path)


class BookPreviewImages(models.Model):
    def book_preview_image(instance, filename):
        ext = filename.split(".")[-1]
        filename = "%s.%s" % ("preview", ext)

        full_path = os.path.join(settings.MEDIA_ROOT, filename)
        if os.path.exists(full_path):
            os.remove(full_path)

        return os.path.join(f"books/preview/{instance.book.title}", filename)

    book = models.ForeignKey(Books, on_delete=models.CASCADE, null=True, blank=True)
    preview_photo = models.ImageField(
        upload_to=book_preview_image, null=True, blank=True
    )

    def __str__(self):
        return self.book.title

    def get_image(self):
        return self.preview_photo.url

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        SIZE = 800, 1400

        if self.preview_photo:
            pic = Image.open(self.preview_photo.path)
            pic.thumbnail(SIZE, Image.LANCZOS)
            pic.save(self.preview_photo.path)


# Changed customer mode; fields to null and blank
class Customers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    contact_no = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    store_credit = models.IntegerField(default=0, null=True, blank=True)
    device = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


# customer  notification 
@receiver(pre_save, sender=Customers)
def before_customer_creation(sender, instance, **kwargs):
    if instance.name == 'guest-auto':
        guest_customers = Customers.objects.filter(name='guest-auto', cart__isnull=True)
        if len(guest_customers) > 800:
            try:
                guest_customers.delete()
            except:
                pass


class Address(models.Model):
    user = models.ForeignKey(Customers, on_delete=models.SET_NULL, null=True)
    district = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    address = models.TextField(null=True, blank=True)
    contact_no = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user.name


class Cart(models.Model):
    user = models.ForeignKey(Customers, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.user.name}  {self.book.title}"

    
    def get_value(self):
        return self.quantity * self.book.exchange_value

    @property
    def price(self):
        return self.book.price

    @property
    def total_amount(self):
        return self.quantity * self.book.price


class Payment(models.Model):
    customer = models.ForeignKey(
        Customers, on_delete=models.SET_NULL, null=True, editable=False)
    sender_number = models.CharField(max_length=15)
    transaction_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=20)
    total_amount = models.FloatField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_id = models.CharField(max_length=100, editable=False)

    def __str__(self):
        return f"{self.payment_method}-{self.transaction_id}-{self.total_amount}"


class Order(models.Model):
    STATUS = (
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Preaparing", "Preaparing"),
        ("OnShipping", "OnShipping"),
        ("Completed", "Completed"),
        ("Canceled", "Canceled"),
    )

    customer = models.ForeignKey(Customers, on_delete=models.SET_NULL, null=True)
    contact_no = models.CharField(max_length=20, blank=True, null=True)
    grand_total = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, blank=True
    )
    order_id = models.CharField(max_length=100)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.customer.name

    def get_shipping_address(self):
        return f"{self.address.address}, {self.address.area}, {self.address.district}"


# Order notification 
@receiver(post_save, sender=Order)
def after_order_change(sender, instance, created, **kwargs):
    def get_address(obj):
        return f"{obj.address.address}, {obj.address.area}, {obj.address.district}"

    def get_ordered_books(obj):
        book_list = []
        for book in obj.ordered_books.all():
            if book.quantity > 1:
                b = f"{book}({book.quantity})"
                book_list.append(b)
            else:
                b = f"{book}"
                book_list.append(b)
                 
        return (", ".join(book_list))

    if not created:
        if instance.status == "Paid":
            new_notif = Notification.objects.create(user=instance.customer, 
            message=f"We’ve confirmed your payment For Order ({instance.order_id}).Thank you for Ordering with us.You can track your order status from my account page.")
            new_notif.save()

            try:
                if not instance.grand_total < 1:
                    tele_text = f"{instance.created_at.strftime('%m/%d/%Y %I:%M %p')}\n\n*বইয়ের নাম : {get_ordered_books(instance)}\n\n*নাম: {instance.customer.name}\nঠিকানা : {get_address(instance)}\nনাম্বার : {instance.contact_no} \n"

                    # print(tele_text)
                    send_tele.send_message(tele_text)
            
            except:
                pass
        
        if instance.status == "Preaparing":
            new_notif = Notification.objects.create(user=instance.customer, 
            message=f"Your order ({instance.order_id}) has been received. To Confirm your order please complete your payment within 2Hours, otherwise your order will be cancelled.To complete order please send ({instance.grand_total})TK amount to 01610427497(Bkash/­Nagad/Rocket)")
            new_notif.save()
        
        if instance.status == "Completed":
            new_notif = Notification.objects.create(user=instance.customer, 
            message=f"Your order ({instance.order_id}) has been delivered. Thank you for Ordering with us.You can give a review at the bottom of your ordered books")
            new_notif.save()





class OrderedProducts(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="ordered_books")
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    books = models.ForeignKey(Books, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    total_amount = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.books.title


class WebSettings(models.Model):
    payment_instruction = RichTextField()
    shipping_charge = models.IntegerField(default=50)
    web_logo = models.ImageField(upload_to="web_logo/", null=True, blank=True)
    exchange_rules = RichTextField(blank=True, null=True)
    show_notification = models.BooleanField(default=False)
    admin_notification = RichTextField(blank=True, null=True)

    def __str__(self):
        return f"Web Settings ( Don't delete it )"


# review model


class Review(models.Model):
    RATING_CHOICES = (
        ("1", 1),
        ("2", 2),
        ("3", 3),
        ("4", 4),
        ("5", 5),
    )

    book = models.ForeignKey(
        Books, on_delete=models.CASCADE, null=True, blank=True, related_name="reviews"
    )
    user = models.ForeignKey(Customers, on_delete=models.CASCADE, null=True, blank=True)
    reviewed_at = models.DateField(auto_now_add=True, blank=True, null=True)
    comment = models.TextField()
    ratings = models.CharField(choices=RATING_CHOICES, max_length=10, default="5")

    def __str__(self):
        return f"{self.book.title} - {self.ratings}"

    class Meta:
        ordering = ('-reviewed_at', )


class QnA(models.Model):
    book = models.ForeignKey(
        Books, on_delete=models.CASCADE, null=True, blank=True, related_name="questions"
    )
    user = models.ForeignKey(Customers, on_delete=models.CASCADE, null=True, blank=True)
    question = models.CharField(max_length=160)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    answer = models.TextField(blank=True)


    class Meta:
        ordering = ('-date', )

    def __str__(self):
        return f"{self.book.title} - {self.user.name}"


# Qna notification 
@receiver(post_save, sender=QnA)
def after_qna_change(sender, instance, created, **kwargs):
    if not created:
        msg = f"Your question About ({instance.book}) has been Answered By AAP. Your Question Answer is : {instance.answer}"
        new_notif = Notification.objects.create(user=instance.user, message=msg, answered=True)
        new_notif.save()



class SavedAddress(models.Model):
    user = models.ForeignKey(
        Customers, on_delete=models.CASCADE, related_name="saved_address"
    )
    name = models.CharField(max_length=160)
    district = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    address = models.TextField(null=True, blank=True)
    contact_no = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user.name


class Exchange(models.Model):

    STATUS = (
        ("Pending", "Pending"),
        ("Granted", "Granted"),
        ("Received", "Received"),
        ("Preaparing", "Preaparing"),
        ("OnShipping", "OnShipping"),
        ("Completed", "Completed"),
        ("Canceled", "Canceled"),
    )
  

    user = models.ForeignKey(
        Customers, on_delete=models.CASCADE, related_name="exchange"
    )
    full_name = models.CharField(max_length=64)
    mobile_no = models.CharField(max_length=15)
    number_of_books = models.IntegerField()
    sending_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS, default="Pending")
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.user.name

# Exchange notification 
@receiver(post_save, sender=Exchange)
def after_exchange_change(sender, instance, created, **kwargs):
    if not created:
        if instance.status == "Preaparing":
            new_notif = Notification.objects.create(user=instance.user, 
            message="তোমার এক্সচেঞ্জ রিকুয়েস্ট গ্রহন করা হয়েছে। তোমাকে এখন বইগুলো নিকটস্থ কুরিয়ারে গিয়ে আমাদের ঠিকানায় পাঠাতে হবে। কুরিয়ারে পাঠানোর তথ্য= নামঃ পাঠশালা লাইব্রেরি, ঠিকানাঃ রাজা বাজার,ঢাকা এবং নাম্বারঃ 01610427498")
            new_notif.save()
        
        if instance.status == "Received":
            new_notif = Notification.objects.create(user=instance.user, 
            message="তোমার এক্সচেঞ্জ রিকুয়েস্ট এর বইগুলো আমরা গ্রহন করেছি। তোমার পাঠানো বইগুলো যাচাই করে আমরা তোমাকে সমতুল্য ক্রেডিট তোমার একাউন্টে দিয়েছি। তুমি My Account অপশনে গিয়ে তোমার প্রাপ্য ক্রেডিট দেখতে পারবে। ক্রেডিট দিয়ে তুমি এক্সচেঞ্জ সেকশন থেকে বই নিতে পারবে।")
            new_notif.save()


# user notification
class Notification(models.Model):
    user = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=260, blank=True, null=True)
    read = models.BooleanField(default=False)
    answered = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def serialize(self):
        return {
            "message": self.message,
            "date" : self.date,
            "answered" : self.answered,
            "read": self.read,
            "id": self.id,
            "name" : self.user.name,
        }

    class Meta:
        ordering = ('-date', )





class AdminNoification(models.Model):
    notification = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return "Admin Notification - Don't reload unless save is complete"




# # Send Admin notification 
# @receiver(post_save, sender=AdminNoification)
# def send_admin_notification(sender, instance, created, **kwargs):
#     customer = Customers.objects.filter(device__isnull=True)
#     for c in customer:
#         new_notif = Notification.objects.create(user=c, message=instance.notification)
#         new_notif.save()
        

   
