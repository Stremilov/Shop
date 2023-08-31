from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ShopIndexView,
    GroupsListView,
    ProductsDetailsView,
    OrdersListView,
    ProductListView,
    OrderDetailView,
    ProductCreateView,
    UpdateProductView,
    ProductDeleteView,
    ExportOrdersView,
    ProductsListViewSet,
    OrdersListViewSet,
)

app_name = 'shopapp'

routers = DefaultRouter()
routers.register("products", ProductsListViewSet)
routers.register('orders', OrdersListViewSet)

urlpatterns = [
    path("", ShopIndexView.as_view(), name='index'),
    path("api/", include(routers.urls)),
    path("groups/", GroupsListView.as_view(), name='groups_list'),
    path("products/", ProductListView.as_view(), name='products_list'),
    path("products/<int:pk>/", ProductsDetailsView.as_view(), name='product_details'),
    path("products/<int:pk>/update/", UpdateProductView.as_view(), name='product_update'),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name='product_delete'),
    path("products/create/", ProductCreateView.as_view(), name='product_create'),
    path("orders/", OrdersListView.as_view(), name='orders_list'),
    path("orders/export/", ExportOrdersView.as_view(), name='orders_export'),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_details"),
]
