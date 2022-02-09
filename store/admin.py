from django.contrib import admin
import admin_thumbnails
from .models import Product,Variation,ReviewRating,ProductGallery


# Register your models here.
@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1
class ProductAdmin(admin.ModelAdmin):
	list_display=('product_name','price','stock','catagory','modified_date','is_available')
	prepopulated_fields={'slug':('product_name',)}
	inlines = [ProductGalleryInline]



class VarationAdmin(admin.ModelAdmin):
	list_display=('product','varation_category','varation_value','is_active')
	list_editable =('is_active',)
	list_filter = ('product','varation_category','varation_value')
admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VarationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)