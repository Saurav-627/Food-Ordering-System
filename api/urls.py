from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'foods', views.FoodViewSet)
router.register(r'orders', views.OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('cart/', views.CartViewSet.as_view({'get': 'list'}), name='api_cart'),
    path('recommendations/personal/', views.RecommendationView.as_view(), name='api_personal_recs'),
    path('recommendations/also-ordered/<int:food_id>/', views.PeopleAlsoOrderedView.as_view(), name='api_also_ordered'),
    path('recommendations/combos/', views.ComboView.as_view(), name='api_combos'),
]
