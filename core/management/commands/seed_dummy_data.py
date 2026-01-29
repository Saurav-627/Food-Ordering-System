from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from foods.models import Category, Food, Rating
from orders.models import Order, OrderItem
import random
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with dummy data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        # Create Users
        admin, _ = User.objects.get_or_create(username='admin', email='admin@example.com', role='ADMIN')
        if not admin.check_password('admin'):
            admin.set_password('admin')
            admin.is_staff = True
            admin.is_superuser = True
            admin.save()
            self.stdout.write('Created admin user (password: admin)')
            
        delivery_boy, _ = User.objects.get_or_create(username='rider', email='rider@example.com', role='DELIVERY_BOY')
        if not delivery_boy.check_password('rider'):
            delivery_boy.set_password('rider')
            delivery_boy.save()
            self.stdout.write('Created delivery boy user (password: rider)')
            
        user1, _ = User.objects.get_or_create(username='user1', email='user1@example.com', role='USER')
        if not user1.check_password('user1'):
            user1.set_password('user1')
            user1.save()
            self.stdout.write('Created normal user (password: user1)')

        # Create Categories
        categories = ['Main Course', 'Snacks', 'Desserts', 'Sides', 'Traditional']
        cat_objs = {}
        for cat_name in categories:
            c, _ = Category.objects.get_or_create(name=cat_name)
            cat_objs[cat_name] = c

        # Create Foods
        foods_data = [
            ("Dal Bhat", "Steamed rice with lentil soup and side dishes.", 180, "Main Course"),
            ("Momo (Chicken)", "Steamed dumplings filled with spiced chicken.", 180, "Snacks"),
            ("Momo (Veg)", "Steamed dumplings with mixed vegetables.", 160, "Snacks"),
            ("Sekuwa", "Grilled marinated meat skewers.", 250, "Snacks"),
            ("Chatamari", "Nepali rice crepe topped with meat or veg.", 140, "Traditional"),
            ("Thukpa", "Hearty noodle soup with vegetables or meat.", 160, "Main Course"),
            ("Sel Roti", "Traditional sweet ring-shaped rice bread.", 40, "Traditional"),
            ("Aloo Tama", "Potato and bamboo shoot curry.", 150, "Main Course"),
            ("Gundruk ko Achar", "Fermented leafy greens pickle.", 90, "Sides"),
            ("Puri Tarkari", "Deep-fried bread with vegetable curry.", 160, "Main Course"),
            ("Bara (wo)", "Lentil pancake topped with egg or meat.", 120, "Traditional"),
            ("Yomari", "Sweet rice dumpling filled with molasses.", 60, "Desserts"),
            ("Kukhura Masu", "Spicy Nepali-style chicken curry.", 240, "Main Course"),
            ("Bhatmas Sadeko", "Spiced roasted soybeans salad.", 80, "Sides"),
            ("Sukuti", "Dried spiced buffalo meat.", 220, "Snacks"),
            ("Masu (Mutton)", "Classic mutton curry.", 260, "Main Course"),
            ("Paneer Tarkari", "Cottage cheese cooked in Nepali spices.", 210, "Main Course"),
            ("Choyela", "Newari spiced grilled meat.", 230, "Traditional"),
            ("Thakali Set", "Balanced platter with rice, curry, pickles.", 300, "Main Course"),
            ("Aloo Chop", "Spiced potato fritter.", 70, "Snacks"),
            ("Laping", "Cold tangy Tibetan-style jelly noodles.", 120, "Snacks"),
            ("Kheer", "Rice pudding with milk and cardamom.", 90, "Desserts"),
            ("Ghee-Smoked Chicken", "Aromatic smoked chicken pieces.", 280, "Main Course"),
            ("Mixed Thali", "Small sampler: 4-5 small dishes.", 350, "Main Course"),
            ("Masu Sadeko", "Spiced stir-fry meat salad.", 200, "Snacks"),
        ]

        food_objs = []
        for name, desc, price, cat_name in foods_data:
            f, created = Food.objects.get_or_create(
                name=name,
                defaults={
                    'description': desc,
                    'price': Decimal(price),
                    'category': cat_objs[cat_name],
                    'prep_time_min': random.randint(10, 40)
                }
            )
            food_objs.append(f)
            
        self.stdout.write(f'Seeded {len(food_objs)} foods')

        # Create dummy orders for recommendations
        # Create 50 orders
        for i in range(50):
            # Random user (create more dummy users if needed, but sticking to user1 for now or creating on fly)
            u, _ = User.objects.get_or_create(username=f'dummy_user_{i}', defaults={'email': f'dummy{i}@example.com', 'role': 'USER'})
            
            o = Order.objects.create(
                user=u,
                status='COMPLETED',
                total_price=0,
                delivery_address='Kathmandu',
                lat=27.7172,
                lng=85.3240
            )
            
            # Add 1-4 items
            items_count = random.randint(1, 4)
            selected_foods = random.sample(food_objs, items_count)
            total = 0
            for food in selected_foods:
                qty = random.randint(1, 2)
                price = food.price * qty
                OrderItem.objects.create(order=o, food=food, quantity=qty, price_at_order=food.price)
                total += price
                
                # Add rating
                if random.random() > 0.5:
                    Rating.objects.create(user=u, food=food, rating=random.randint(3, 5))
            
            o.total_price = total
            o.save()

        self.stdout.write(self.style.SUCCESS('Successfully seeded data'))
