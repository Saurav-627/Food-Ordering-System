from django.shortcuts import render, get_object_or_404, redirect
from foods.models import Category, Food, Rating
from django.contrib.auth.decorators import login_required
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
    ratings = food.ratings.all().order_by('-created_at')
    
    avg_rating = 0
    if ratings.exists():
        avg_rating = sum(r.rating for r in ratings) / ratings.count()
    
    context = {
        'food': food,
        'related_foods': related_foods,
        'ratings': ratings,
        'avg_rating': round(avg_rating, 1),
        'rating_count': ratings.count(),
    }
    return render(request, 'core/food_detail.html', context)

def presentation(request):
    return render(request, 'core/presentation.html')

@login_required
def submit_review(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    if request.method == 'POST':
        rating_value = request.POST.get('rating')
        review_text = request.POST.get('review')
        
        if rating_value:
            Rating.objects.update_or_create(
                user=request.user,
                food=food,
                defaults={
                    'rating': int(rating_value),
                    'review': review_text
                }
            )
            from django.contrib import messages
            messages.success(request, "Your review has been submitted.")
        else:
            from django.contrib import messages
            messages.error(request, "Please provide a rating.")
            
    return redirect('food_detail', slug=food.slug)
