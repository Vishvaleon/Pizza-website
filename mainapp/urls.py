from django.urls import path
from .import views
urlpatterns = [
    path('', views.HomePage.as_view() , name='home'),
    path('pizza/<int:pk>', views.PizzaDetails.as_view() , name='pizza_detail'),
    path('order_pizza/<int:id>/<int:user_id>', views.pizza_order, name='order_pizza'),
    path('order/<int:id>', views.view_orders , name = 'order'),
    path('add_cart/<int:pizza_id>/<int:user_id>', views.add_cart, name='add_cart'),
    path('my_cart/<int:user_id>', views.mycart, name='my_cart'),
    path('update_cart/<int:cart_id>/', views.update_cart, name='update_cart'),
    path('delete_cart/<int:cart_id>', views.delete_cart,  name='delete_cart'),
    path('checkout/<int:user_id>/', views.checkout, name='checkout'),
    path('confirm_order/<int:user_id>/', views.confirm_order, name='confirm_order'),
]