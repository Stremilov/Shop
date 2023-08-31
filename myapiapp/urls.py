from django.urls import path

from .views import ProductsListView, OrdersListView

app_name = 'myapi'


urlpatterns = [
    path('products/', ProductsListView.as_view(), name='show_products'),
    path('orders/', OrdersListView.as_view(), name='show_orders'),
]

