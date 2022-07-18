from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

# Register your models here.
from .models import *


# This shows all review for a book


class Main_CategoryAdmin(admin.ModelAdmin):
    list_display = ('__str__','slug',)
    prepopulated_fields = {"slug": ("name",)}
class Sub_CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('__str__','parent_category','slug',)


class PreviewImagesTabularAdmin(admin.TabularInline):
    model = BookPreviewImages
    fields = ("book", "preview_photo",)

    

class BooksAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

    list_display = ('__str__', 'main_category','get_category','price','in_stock','serial_number', 'exchange_value', 'exchangeable_stock', 'free_delivery')
    list_filter = ('category','category__parent_category')

    list_editable = ('price','in_stock','serial_number', 'exchange_value', 'exchangeable_stock', 'free_delivery')

    inlines = [PreviewImagesTabularAdmin]

    def get_category(self, obj):
        return ", ".join([p.name for p in obj.category.all()])
    
    def main_category(self, obj):
        return ", ".join({p.parent_category.name for p in obj.category.all()})

    get_category.short_description = "Categories"
    get_category.main_category = "Main Category"




admin.site.register(Main_Category,Main_CategoryAdmin)
admin.site.register(Sub_Category,Sub_CategoryAdmin)
admin.site.register(Books,BooksAdmin)



class CustomerFilter(admin.SimpleListFilter):
    title = _('Customer Type')
    parameter_name = 'customer_guest'

    def lookups(self, request, model_admin):

        return (
            ('Guest', _('Show Only Guest')),
        )

    def queryset(self, request, queryset):

        if self.value() == 'Guest':
            return queryset.filter(name='guest-auto')


class CustomersAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_no', 'store_credit')
    list_editable = ('store_credit',)
    search_fields = ['contact_no']

    list_filter = (CustomerFilter,)

    

admin.site.register(Customers,CustomersAdmin)


class AddressAdmin(admin.ModelAdmin):
    readonly_fields = ('user',)

admin.site.register(Address,AddressAdmin)

class CartAdmin(admin.ModelAdmin):
    readonly_fields = ('user','book',)
    list_display = ('__str__','book','quantity',)
admin.site.register(Cart,CartAdmin)



class OrderedBooksAdmin(admin.TabularInline):
    model = OrderedProducts
    fields = ("books", "quantity","price","total_amount")
    readonly_fields = ("books", "quantity","price","total_amount")
    extra = 0
    


class ExchangeOrderFilter(admin.SimpleListFilter):
    title = _('Payment Type')
    parameter_name = 'payment_typ'

    def lookups(self, request, model_admin):

        return (
            ('Exchange', _('Hide All Exchange Order')),
        )

    def queryset(self, request, queryset):

        if self.value() == 'Exchange':
            return queryset.filter(~Q(payment__payment_method="Exchange"))
     

class OrderAdmin(admin.ModelAdmin):
    
    list_display = ('__str__','contact_no','grand_total','get_address','payment_details','status', 'created_at', 'ordered_books')
    readonly_fields = ('customer','grand_total','order_id','address','payment','contact_no')
    list_editable = ('status',)
    inlines = [OrderedBooksAdmin]
    search_fields = ['payment__transaction_id', 'contact_no', 'customer__name']

    list_filter = ('payment__payment_method', ExchangeOrderFilter)

    def get_address(self,obj):
        return f"{obj.address.address}, {obj.address.area}, {obj.address.district}"

    def payment_details(self,obj):
        return f"({obj.payment.payment_method})- ({obj.payment.sender_number}) - TRXID: {obj.payment.transaction_id}"

    def ordered_books(self, obj):
        book_list = []
        for book in obj.ordered_books.all():
            if book.quantity > 1:
                b = f"{book}({book.quantity})"
                book_list.append(b)
            else:
                b = f"{book}"
                book_list.append(b)
                 
        return book_list
    
    get_address.short_description = "Shipping"

    


admin.site.register(Order,OrderAdmin)





class PaymentAdmin(admin.ModelAdmin):
    
    list_display = ('__str__','sender_number','transaction_id','payment_method','total_amount','order_id')
    readonly_fields = ('sender_number','transaction_id','payment_method','total_amount','order_id',)


admin.site.register(Payment,PaymentAdmin)


class OrderedProductsAdmin(admin.ModelAdmin):
    list_display = ('__str__','customer')
    readonly_fields = ('customer','order','books','quantity','price','total_amount')
    

admin.site.register(OrderedProducts,OrderedProductsAdmin)


admin.site.register(WebSettings)


# review admin 

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('__str__','user','comment',)
    readonly_fields = ('book','user',)

admin.site.register(Review,ReviewAdmin)

# QA admin

class QnAAdmin(admin.ModelAdmin):
    list_display = ('__str__','question','answer',)
    readonly_fields = ('book','user',)


admin.site.register(QnA,QnAAdmin)


class ExchangeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'mobile_no', 'number_of_books', 'sending_date', 'comment', 'status',)
    list_editable = ('status',)

    search_fields = ['mobile_no']




admin.site.register(Exchange, ExchangeAdmin)


admin.site.register(SavedAddress)



# author and publisher admin 

class AuhtorAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class PublisherAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Author, AuhtorAdmin)
admin.site.register(Publisher, PublisherAdmin)
# admin.site.register(AdminNoification)

