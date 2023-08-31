from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, TemplateView, ListView, UpdateView, DetailView
from django.utils.translation import gettext as _

from shopapp.models import Order
# from .forms import UserCreate
from .models import Profile


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('myauth:about-me')

    def form_valid(self, form):
        response = super().form_valid(form)

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        Profile.objects.create(user=self.object)
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(self.request, user=user)
        return response


class AboutMeView(DetailView):
    template_name = 'myauth/about-me.html'
    model = User


class LogoutUserView(LogoutView):
    next_page = reverse_lazy('myauth:login')



def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse('Cookie set')
    response.set_cookie('foo', 'bar', max_age=1200)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('foo', 'default value')
    return HttpResponse(f'Cookie value: {value}')


def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session['foo'] = 'bar'
    return HttpResponse('Session set')


def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get('foo', 'default')
    return HttpResponse(f'Session value {value}')


class ShowUsersView(ListView, UserPassesTestMixin):
    model = User
    permission_required(User.is_staff)
    template_name = 'myauth/profile_list.html'
    context_object_name = 'users_list'


class UpdateUserInfoView(UpdateView, LoginRequiredMixin, UserPassesTestMixin, User):

    def test_func(self):
        return self.request.user.is_superuser or permission_required('change_profile', raise_exception=True)

    model = Profile
    fields = 'username', 'first_name', 'email', 'bio', 'avatar'
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('myauth:about-user-pk', kwargs={'pk': self.object.user.pk})


class UserDetailsView(DetailView, LoginRequiredMixin):
    model = User
    login_required(lambda user: user.is_authenticated)
    template_name = "myauth/profile_update_form.html"
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class HelloView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        message = _('Hello world!')
        return HttpResponse(f'<h1>{message}</h1>')