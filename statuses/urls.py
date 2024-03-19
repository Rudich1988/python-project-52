from django.urls import path

from .views import StatusesCreateView, StatusesShowView, StatusDeleteView, StatusUpdateView, StatusDeleteErrorTemplateView


app_name = 'statuses'

urlpatterns = [
    path('', StatusesShowView.as_view(), name='statuses_show'),
    path('create/', StatusesCreateView.as_view(), name='status_create'),
    path('<int:pk>/delete/', StatusDeleteView.as_view(), name='status_delete'),
    path('<int:pk>/update/', StatusUpdateView.as_view(), name='status_update'),
    path('<int:pk>/delete', StatusDeleteErrorTemplateView.as_view(), name='status_delete_error'),
]