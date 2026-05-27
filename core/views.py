from django.shortcuts import render, get_object_or_404, redirect
from foods.models import Category, Food, Rating
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from .algorithms import quick_sort, binary_search

def home(request):
    categories = Category.objects.all()
    featured_foods = Food.objects.filter(is_available=True).order_by('?')[:4]
    
    # Algorithm #3: Frequency Counting Algorithm for Most Preferred Items (Global)
    most_preferred = Food.objects.annotate(
        unique_customer_count=Count('order_items__order__user', distinct=True)
    ).order_by('-unique_customer_count')[:4]

    personalized_recs = []
    if request.user.is_authenticated:
        from recommendations.utils import get_recommendations_for_user
        personalized_recs = get_recommendations_for_user(request.user.id, top_n=4)
    
    context = {
        'categories': categories,
        'featured_foods': featured_foods,
        'most_preferred': most_preferred,
        'personalized_recs': personalized_recs,
    }
    return render(request, 'core/home.html', context)

def food_list(request):
    category_slug = request.GET.get('category')
    search_query = request.GET.get('search')
    sort_by = request.GET.get('sort')
    
    foods = Food.objects.filter(is_available=True)
    
    if category_slug:
        foods = foods.filter(category__slug=category_slug)
        
    if search_query:
        # Perform exact‑match search using custom binary_search algorithm
        # Ensure we have a sorted list of food names (case‑insensitive)
        sorted_foods = list(foods.order_by('name'))
        name_list = [f.name.lower() for f in sorted_foods]
        idx = binary_search(name_list, search_query.lower())
        if idx is not None:
            # Exact match found – return a queryset containing that single food
            foods = Food.objects.filter(id=sorted_foods[idx].id)
        else:
            # No exact match – return empty queryset
            foods = Food.objects.none()
        
    # Algorithmic sorting using quick_sort (client‑side)
    # Convert queryset to list for in‑memory sorting
    food_list = list(foods)
    if sort_by == 'price_low':
        food_list = quick_sort(food_list, key=lambda f: f.price)
    elif sort_by == 'price_high':
        food_list = quick_sort(food_list, key=lambda f: -f.price)
    elif sort_by == 'name_az':
        food_list = quick_sort(food_list, key=lambda f: f.name.lower())
    elif sort_by == 'name_za':
        food_list = quick_sort(food_list, key=lambda f: f.name.lower())
        food_list.reverse()
    else:
        food_list = quick_sort(food_list, key=lambda f: f.created_at)
        food_list.reverse()
    foods = food_list
        
    categories = Category.objects.all()
    
    context = {
        'foods': foods,
        'categories': categories,
        'current_category': category_slug,
        'search_query': search_query,
        'current_sort': sort_by,
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
