from operator import mod
from pickle import TRUE
from pyexpat import model
from random import choices
from django.db import models
from django.contrib.auth.models import User
import os
from PIL import Image
from django.conf import settings
import uuid

from ckeditor.fields import RichTextField
from django.forms import CharField, ChoiceField

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
    serial_number = models.IntegerField(null=True, blank=True)
    preparation = models.CharField(max_length=260,null=True, blank=True)

    def __str__(self):
        return self.title

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


class Customers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=20)
    email = models.EmailField(max_length=50, null=True, blank=True)
    store_credit = models.IntegerField(default=0)

    def __str__(self):
        return self.name


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

    @property
    def price(self):
        return self.book.price

    @property
    def total_amount(self):
        return self.quantity * self.book.price


class Payment(models.Model):
    customer = models.ForeignKey(
        Customers, on_delete=models.SET_NULL, null=True, editable=False
    )
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


class OrderedProducts(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
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
    exchange_rules = models.TextField(blank=True, null=True)

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
    reviewed_at = models.DateField(auto_now_add=True)
    comment = models.TextField()
    ratings = models.CharField(choices=RATING_CHOICES, max_length=10, default="5")

    def __str__(self):
        return f"{self.book.title} - {self.ratings}"


class QnA(models.Model):
    book = models.ForeignKey(
        Books, on_delete=models.CASCADE, null=True, blank=True, related_name="questions"
    )
    user = models.ForeignKey(Customers, on_delete=models.CASCADE, null=True, blank=True)
    question = models.CharField(max_length=160)
    date = models.DateTimeField(auto_now_add=True, null=True)
    answer = models.TextField(blank=True)

    def __str__(self):
        return f"{self.book.title} - {self.user.name}"


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
        ("Received", "Received"),
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
