from django.contrib import admin

# Register your models here.
from .models import *

class Main_CategoryAdmin(admin.ModelAdmin):
    list_display = ('__str__','slug',)
    prepopulated_fields = {"slug": ("name",)}
class Sub_CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('__str__','parent_category','slug',)

class BooksAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

    list_display = ('__str__', 'main_category','get_category','price',)
    list_filter = ('category','category__parent_category')
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
    readonly_fields = ('user',)

admin.site.register(Customers,CustomersAdmin)


class AddressAdmin(admin.ModelAdmin):
    readonly_fields = ('user',)

admin.site.register(Address,AddressAdmin)

class CartAdmin(admin.ModelAdmin):
    readonly_fields = ('user','book',)
    list_display = ('__str__','book','quantity',)
admin.site.register(Cart,CartAdmin)



admin.site.register(Order)
admin.site.register(OrderedProducts)