from rest_framework import viewsets, permissions, views, response
from foods.models import Category, Food
from orders.models import Cart, Order
from .serializers import CategorySerializer, FoodSerializer, CartSerializer, OrderSerializer
from recommendations.utils import get_recommendations_for_user, get_people_also_ordered
from orders.utils import get_cart

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class FoodViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Food.objects.filter(is_available=True)
    serializer_class = FoodSerializer
    filterset_fields = ['category']
    search_fields = ['name', 'description']

class CartViewSet(viewsets.ViewSet):
    def list(self, request):
        cart = get_cart(request)
        serializer = CartSerializer(cart)
        return response.Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class RecommendationView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Personal
        personal_recs = get_recommendations_for_user(request.user.id)
        personal_serializer = FoodSerializer(personal_recs, many=True)
        
        return response.Response({
            'personal_recommendations': personal_serializer.data
        })

class PeopleAlsoOrderedView(views.APIView):
    def get(self, request, food_id):
        recs = get_people_also_ordered(food_id)
        serializer = FoodSerializer(recs, many=True)
        return response.Response(serializer.data)

class ComboView(views.APIView):
    def get(self, request):
        # Simple combo logic: Get items in cart, find most co-occurring item not in cart
        cart = get_cart(request)
        if not cart.items.exists():
            return response.Response({'message': 'Cart is empty'})
            
        cart_food_ids = list(cart.items.values_list('food_id', flat=True))
        suggestions = []
        
        for food_id in cart_food_ids:
            recs = get_people_also_ordered(food_id, top_n=2)
            for rec in recs:
                if rec.id not in cart_food_ids and rec not in suggestions:
                    suggestions.append(rec)
        
        # Limit to 3 suggestions
        suggestions = suggestions[:3]
        
        data = []
        for food in suggestions:
            data.append({
                'food': FoodSerializer(food).data,
                'discount_price': float(food.price) * 0.9, # 10% off
                'savings': float(food.price) * 0.1
            })
            
        return response.Response({'combos': data})
