import os
import django
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'khaja_kham.settings')
django.setup()

from foods.models import Food, Category, Rating
from users.models import User
from orders.models import Order, OrderItem

def seed_complete_data():
    # 1. Ensure categories and foods exist
    # Mapping of food names to image filenames (must match files in media/foods)
    image_map = {
        'Momo': 'momo.png',
        'Thakali Set': 'thakali-set.png',
        'Sel Roti': 'sel-roti.png',
        'Burger': 'burger.png',
        'Pizza': 'pizza.png',
        'Fries': 'fries.png',
        'Coke': 'coke.png',
        'Lassi': 'lassi.png',
        'Ice Cream': 'ice-cream.png',
    }
    categories = ['Nepali Specials', 'Fast Food', 'Beverages', 'Desserts']
    for cat_name in categories:
        Category.objects.get_or_create(name=cat_name)
    
    # 2. Get/Create Users
    usernames = ['Saurav', 'Ankit', 'Maya', 'John', 'Deepa', 'Rahul']
    users = []
    for uname in usernames:
        user, _ = User.objects.get_or_create(username=uname, defaults={'email': f'{uname.lower()}@test.com'})
        users.append(user)
    
    # 3. Create diverse Food items
    food_data = [
        ('Momo', 'Nepali Specials', 150),
        ('Thakali Set', 'Nepali Specials', 450),
        ('Sel Roti', 'Nepali Specials', 50),
        ('Burger', 'Fast Food', 250),
        ('Pizza', 'Fast Food', 600),
        ('Fries', 'Fast Food', 120),
        ('Coke', 'Beverages', 60),
        ('Lassi', 'Beverages', 100),
        ('Ice Cream', 'Desserts', 150),
    ]
    
    foods = []
    for name, cat_name, price in food_data:
        cat = Category.objects.get(name=cat_name)
        img_filename = image_map.get(name)
        defaults = {'category': cat, 'price': price, 'description': f'Delicious {name}'}
        if img_filename:
            defaults['image'] = f'foods/{img_filename}'
        food, _ = Food.objects.update_or_create(
            name=name,
            defaults=defaults,
        )
        foods.append(food)

    # 4. Create Random Ratings (for Collaborative Filtering)
    # Pattern: Some users like Nepali specials, some like Fast Food
    for user in users:
        preferred_cat = random.choice(categories)
        for food in foods:
            if food.category.name == preferred_cat:
                rating = random.randint(4, 5) # High rating for preference
            else:
                rating = random.randint(1, 4) # Lower/Random for others
            
            Rating.objects.update_or_create(
                user=user, food=food, 
                defaults={'rating': rating}
            )

    # 5. Create Completed Orders (for Co-occurrence / 'People also ordered')
    # Pattern: Coke is often bought with Burger or Pizza
    coke = Food.objects.get(name='Coke')
    burger = Food.objects.get(name='Burger')
    pizza = Food.objects.get(name='Pizza')
    
    for i in range(10):
        user = random.choice(users)
        order = Order.objects.create(user=user, total_price=0, status='COMPLETED')
        
        # Add Burger + Coke
        OrderItem.objects.create(order=order, food=burger, quantity=1, price_at_order=burger.price)
        OrderItem.objects.create(order=order, food=coke, quantity=1, price_at_order=coke.price)
        
    print("Database seeded with realistic patterns.")

if __name__ == "__main__":
    seed_complete_data()
