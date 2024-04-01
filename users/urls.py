from django.urls import path

from .views import UserRegistrationView, UsersShowView, UserDeleteView, UserUpdateView


app_name = 'users'

urlpatterns = [
    path('', UsersShowView.as_view(), name='users_show'),
    path('create/', UserRegistrationView.as_view(), name='create_user'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
]