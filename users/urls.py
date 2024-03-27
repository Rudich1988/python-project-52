from django.urls import path

from .views import UserRegistrationView, UsersShowView, UserDeleteView, UserUpdateView, UserDeleteTemplateView


app_name = 'users'
#mm

urlpatterns = [
    path('', UsersShowView.as_view(), name='users_show'),
    path('create/', UserRegistrationView.as_view(), name='create_user'),
    #path('<int:pk>/delete', UserDeleteTemplateView.as_view(), name='user_delete_template'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
]