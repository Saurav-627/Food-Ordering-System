import os
import django
import shutil

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'khaja_kham.settings')
django.setup()

from django.contrib.auth import get_user_model
from foods.models import Food, Category, Rating
from orders.models import Order, OrderItem, Cart, CartItem
from django.core.files import File
from django.utils.text import slugify

User = get_user_model()

def clear_data():
    print("Clearing old data and cleaning media/foods/...")
    OrderItem.objects.all().delete()
    Order.objects.all().delete()
    CartItem.objects.all().delete()
    Cart.objects.all().delete()
    Rating.objects.all().delete()
    Food.objects.all().delete()
    Category.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()
    
    # Wipe the media/foods directory to prevent duplicates like buff-momo_abc.png
    media_foods_path = os.path.join('media', 'foods')
    if os.path.exists(media_foods_path):
        for filename in os.listdir(media_foods_path):
            file_path = os.path.join(media_foods_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
    print("Old data and media files cleared.")

def create_users():
    print("Creating users (rider & saurav)...")
    rider, created = User.objects.get_or_create(
        username='rider',
        defaults={'role': 'DELIVERY_BOY', 'phone': '9800000001', 'address': 'Koteshwor, Kathmandu'}
    )
    rider.set_password('rider123')
    rider.role = 'DELIVERY_BOY'
    rider.save()

    customer, created = User.objects.get_or_create(
        username='saurav',
        defaults={'role': 'USER', 'phone': '9800000002', 'address': 'Patan, Lalitpur'}
    )
    customer.set_password('saurav123')
    customer.role = 'USER'
    customer.save()
    print("Users created.")

def create_nepali_foods():
    print("Creating Nepali food entries from seed_assets...")
    cat_specials, _ = Category.objects.get_or_create(
        name="Nepali Specials",
        description="Authentic flavors from the heart of Nepal."
    )

    food_data = [
        {
            'name': 'Buff Momo',
            'description': 'Juicy Buff Momo (steamed dumplings) served with a small bowl of spicy orange tomato chutney in the center, garnished with fresh cilantro, traditional Nepali style.',
            'price': 150.00,
            'image_file': 'buff-momo.png',
            'prep_time': 20
        },
        {
            'name': 'Thakali Set',
            'description': 'Authentic Nepali Thakali Thali set on a brass plate (Thal), including steamed rice, yellow lentil soup (Dal), sautéed spinach (Saag), spicy potato fries (Aloo Fry), radish pickle (Mula ko Achar), and a small bowl of chicken curry.',
            'price': 450.00,
            'image_file': 'thakali-set.png',
            'prep_time': 30
        },
        {
            'name': 'Newari Khaja Set',
            'description': 'Traditional Newari Khaja Set on a leaf plate (Tapari), featuring beaten rice (Chiura), spiced smoked meat (Choila), black soybeans (Bhatmas Sandheko), boiled egg, spiced potato (Aloo Sandheko), and fermented bamboo shoot curry (Tama).',
            'price': 350.00,
            'image_file': 'newari-khaja.png',
            'prep_time': 25
        },
        {
            'name': 'Sel Roti with Curry',
            'description': 'A stack of golden-brown Nepali Sel Roti (ring-shaped sweet fried rice bread) served with a side of spicy dry potato curry (Aloo ko Achar), traditional Nepali festival food.',
            'price': 120.00,
            'image_file': 'sel-roti.png',
            'prep_time': 15
        },
        {
            'name': 'Chatamari',
            'description': "Nepali Chatamari (rice crepe) topped with minced meat, sliced boiled egg, and chopped green onions, often known as 'Nepali Pizza'.",
            'price': 180.00,
            'image_file': 'chatamari.png',
            'prep_time': 15
        },
    ]

    for item in food_data:
        food = Food.objects.create(
            category=cat_specials,
            name=item['name'],
            description=item['description'],
            price=item['price'],
            prep_time_min=item['prep_time'],
            is_available=True
        )
        # Load image from seed_assets/foods/
        asset_path = os.path.join('seed_assets', 'foods', item['image_file'])
        if os.path.exists(asset_path):
            with open(asset_path, 'rb') as f:
                food.image.save(item['image_file'], File(f), save=True)
            print(f"Added food item with image: {item['name']}")
        else:
            print(f"Asset missing for {item['name']}, adding without image.")

if __name__ == '__main__':
    clear_data()
    create_users()
    create_nepali_foods()
    print("\nProject Seeding Done! Media folder is clean and duplicates removed.")
