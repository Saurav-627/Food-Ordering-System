import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from orders.models import Order, OrderItem
from foods.models import Food, Rating
from .models import RecommendationCache
import json

def get_item_similarity_matrix():
    try:
        cache = RecommendationCache.objects.get(key='item_similarity')
        return pd.DataFrame(cache.data)
    except RecommendationCache.DoesNotExist:
        return pd.DataFrame()

def get_co_occurrence_matrix():
    try:
        cache = RecommendationCache.objects.get(key='co_occurrence')
        return pd.DataFrame(cache.data)
    except RecommendationCache.DoesNotExist:
        return pd.DataFrame()

def train_item_similarity():
    # Build user-item matrix from Ratings
    ratings = Rating.objects.all().values('user_id', 'food_id', 'rating')
    if not ratings:
        return
    
    df = pd.DataFrame(ratings)
    user_item_matrix = df.pivot_table(index='user_id', columns='food_id', values='rating').fillna(0)
    
    # Compute cosine similarity between items (transpose to get item-item)
    item_similarity = cosine_similarity(user_item_matrix.T)
    item_similarity_df = pd.DataFrame(item_similarity, index=user_item_matrix.columns, columns=user_item_matrix.columns)
    
    # Save to cache
    RecommendationCache.objects.update_or_create(
        key='item_similarity',
        defaults={'data': item_similarity_df.to_dict()}
    )
    print("Item similarity matrix updated.")

def train_co_occurrence():
    # Build co-occurrence from Orders
    orders = Order.objects.filter(status='COMPLETED')
    
    co_occurrence = {}
    
    for order in orders:
        items = list(order.items.values_list('food_id', flat=True))
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                item_a, item_b = items[i], items[j]
                
                # Ensure consistent ordering for keys
                pair = tuple(sorted((item_a, item_b)))
                
                if item_a not in co_occurrence: co_occurrence[item_a] = {}
                if item_b not in co_occurrence: co_occurrence[item_b] = {}
                
                co_occurrence[item_a][item_b] = co_occurrence[item_a].get(item_b, 0) + 1
                co_occurrence[item_b][item_a] = co_occurrence[item_b].get(item_a, 0) + 1
                
    # Save to cache (convert to simpler format if needed, or just dict)
    RecommendationCache.objects.update_or_create(
        key='co_occurrence',
        defaults={'data': co_occurrence}
    )
    print("Co-occurrence matrix updated.")

def get_recommendations_for_user(user_id, top_n=5):
    # Simple logic: get user's last rated/ordered item, find similar items
    # Better logic: Weighted sum of similar items
    
    # For now, let's use the last item user interacted with
    last_rating = Rating.objects.filter(user_id=user_id).order_by('-created_at').first()
    if not last_rating:
        return []
        
    sim_matrix = get_item_similarity_matrix()
    if sim_matrix.empty:
        return []
        
    food_id = str(last_rating.food_id) # Pandas columns might be strings if loaded from JSON
    if food_id not in sim_matrix.columns:
        # Try int
        food_id = last_rating.food_id
        if food_id not in sim_matrix.columns:
            return []
            
    similar_scores = sim_matrix[food_id].sort_values(ascending=False)
    similar_items = similar_scores.index[1:top_n+1] # Exclude self
    
    return Food.objects.filter(id__in=similar_items)

def get_people_also_ordered(food_id, top_n=4):
    co_matrix = get_co_occurrence_matrix()
    if co_matrix.empty:
        return []
        
    # Check if food_id exists in columns (might need string conversion)
    fid = str(food_id)
    if fid not in co_matrix.columns:
        fid = int(food_id)
        if fid not in co_matrix.columns:
            return []
            
    # Get top co-occurring
    related = co_matrix[fid].sort_values(ascending=False).head(top_n)
    return Food.objects.filter(id__in=related.index)
