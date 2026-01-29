from django.shortcuts import render, get_object_or_404
from foods.models import Category, Food
from django.db.models import Q

def home(request):
    categories = Category.objects.all()
    featured_foods = Food.objects.filter(is_available=True).order_by('?')[:4] # Random for now
    context = {
        'categories': categories,
        'featured_foods': featured_foods,
    }
    return render(request, 'core/home.html', context)

def food_list(request):
    category_slug = request.GET.get('category')
    search_query = request.GET.get('search')
    
    foods = Food.objects.filter(is_available=True)
    
    if category_slug:
        foods = foods.filter(category__slug=category_slug)
        
    if search_query:
        foods = foods.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
        
    categories = Category.objects.all()
    
    context = {
        'foods': foods,
        'categories': categories,
        'current_category': category_slug,
        'search_query': search_query,
    }
    return render(request, 'core/food_list.html', context)

def food_detail(request, slug):
    food = get_object_or_404(Food, slug=slug)
    related_foods = Food.objects.filter(category=food.category).exclude(id=food.id)[:4]
    
    context = {
        'food': food,
        'related_foods': related_foods,
    }
    return render(request, 'core/food_detail.html', context)
