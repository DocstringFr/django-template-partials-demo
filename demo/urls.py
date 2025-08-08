from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='index'),
    path('like-counter/', csrf_exempt(views.like_counter), name='like-counter'),
    path('update-content/', views.update_content, name='update-content'),
    path('online-status/', views.online_status, name='online-status'),
    path('cart/add/<int:product_id>/', csrf_exempt(views.add_to_cart), name='add-to-cart'),
    path('cart/remove/<int:product_id>/', csrf_exempt(views.remove_from_cart), name='remove-from-cart'),
]
