from django.contrib import admin
from .models import Category, Product, Review, Order, Cart,Job

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_category')
    list_filter = ('parent_category',)
    search_fields = ('name',)

    # Optional: To make subcategories editable inline in the admin interface
    # This will let you add subcategories directly when creating or editing a category
    class SubCategoryInline(admin.TabularInline):
        model = Category
        fk_name = 'parent_category'
        extra = 1  # Number of extra empty forms for new subcategories

    inlines = [SubCategoryInline]

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price')
    list_filter = ('category',)
    search_fields = ('name', 'description')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Job)

