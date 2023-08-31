import json

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from timeit import default_timer
from django.contrib.auth.models import Group, User
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from myapiapp.cerializers import ProductSerializer, OrderSerializer
from .models import Models, Order

from .forms import ProductCreate, GroupForm


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Phone', 3999),
        ]
        context = {
            'time_running': default_timer(),
            'products': products
        }
        return render(request, 'shopapp/shop-index.html', context=context)


class GroupsListView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": GroupForm(),
            "groups": Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)


class ProductsDetailsView(LoginRequiredMixin, DetailView):
    login_required(lambda user: user.is_authenticated)
    template_name = "shopapp/products-details.html"
    model = Models
    context_object_name = 'product'


class ProductListView(LoginRequiredMixin, ListView):
    login_required(lambda user: user.is_authenticated)
    template_name = "shopapp/products-list.html"
    context_object_name = 'products'
    queryset = Models.objects.filter(archived=True)


class ProductCreateView(LoginRequiredMixin, CreateView):
    permission_required('add_product', raise_exception=True)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    model = Models
    fields = 'name', 'description', 'price', 'discount', 'preview'
    success_url = reverse_lazy('shopapp:products_list')


class UpdateProductView(UserPassesTestMixin, UpdateView, LoginRequiredMixin):
    login_required(lambda user: user.is_authenticated)

    def test_func(self):
        return self.request.user.is_superuser or permission_required('change_product', raise_exception=True)
    model = Models
    fields = 'name', 'description', 'price', 'discount', 'preview'
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('shopapp:product_details', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    login_required(lambda user: user.is_authenticated)
    model = Models
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrdersListView(LoginRequiredMixin, ListView):
    login_required(lambda user: user.is_authenticated)
    context_object_name = 'orders'
    queryset = (Order.objects.select_related('user').prefetch_related('products'))


class OrderDetailView(LoginRequiredMixin, DetailView):
    login_required(lambda user: user.is_authenticated)
    queryset = (Order.objects.select_related('user').prefetch_related('products'))


class ExportOrdersView(View, UserPassesTestMixin):
    permission_required(User.is_staff)

    def get(self, request: HttpRequest):
        orders = Order.objects.all()
        return render(request, 'shopapp/order_list.html')


class ProductsListViewSet(ModelViewSet):
    """
    Products
    """

    filter_backends = [
        SearchFilter,
        OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = ['name']
    filterset_fields = [
        'name',
        'description',
        'price',
        'discount',
        'archived',
    ]
    queryset = Models.objects.all()
    serializer_class = ProductSerializer

    @extend_schema(responses={
            200: ProductSerializer,
            404: OpenApiResponse(description='Empty response')
        }
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class OrdersListViewSet(ModelViewSet):
    filter_backends = [
        SearchFilter,
        OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = ['name']
    filterset_fields = [
        'delivery_adress',
        'promocode',
        'created_time',
        'products',
        'reciept',
    ]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
