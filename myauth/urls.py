from django.contrib.auth.views import LoginView
from django.urls import path

from .views import set_session_view, get_session_view, set_cookie_view, get_cookie_view, LogoutUserView, RegisterView, AboutMeView, ShowUsersView, UpdateUserInfoView, HelloView

app_name = 'myauth'

urlpatterns = [
    path('login/',
         LoginView.as_view(
        template_name='myauth/login.html',
        redirect_authenticated_user=True,
    ),
     name='login'),
    path('hello/', HelloView.as_view(), name='hello'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('about-me/', AboutMeView.as_view(), name='about-me'),
    path('about-user/<int:pk>', AboutMeView.as_view(), name='about-user-pk'),
    path('about-me/<int:pk>/update/', UpdateUserInfoView.as_view(), name='update_user_info'),
    path('cookie/set/', set_cookie_view, name='set-cookie'),
    path('cookie/get/', get_cookie_view, name='get-cookie'),
    path('session/set/', set_session_view, name='set-session'),
    path('session/get/', get_session_view, name='get-session'),
    path('users/', ShowUsersView.as_view(), name='show_users'),
    # path("profile/", UserProfile.as_view(), name='user_profile'),

]