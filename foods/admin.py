from django.contrib import admin
from .models import Category, Food, Rating

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available']
    list_filter = ['category', 'is_available']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'food', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
