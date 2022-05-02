from django.contrib import admin

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

    list_display = ('__str__', 'main_category','get_category','price','in_stock',)
    list_filter = ('category','category__parent_category')

    list_editable = ('price','in_stock',)

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


class CustomersAdmin(admin.ModelAdmin):
    # readonly_fields = (,)
    pass

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
    


class OrderAdmin(admin.ModelAdmin):
    
    list_display = ('__str__','contact_no','grand_total','get_address','payment_details','status')
    readonly_fields = ('customer','grand_total','order_id','address','payment','contact_no')

    list_editable = ('status',)

    inlines = [OrderedBooksAdmin]

    search_fields = ('payment__transaction_id',)

    def get_address(self,obj):
        return f"{obj.address.district}-{obj.address.area},{obj.address.address}"

    def payment_details(self,obj):
        return f"({obj.payment.payment_method})- ({obj.payment.sender_number}) - TRXID: {obj.payment.transaction_id}"
    
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





