from django.urls import path
from .views import PublicPostListView, UserPostCreateView, PostDeleteView

urlpatterns = [
    path('', PublicPostListView.as_view(), name='post-list'),
    path('create/', UserPostCreateView.as_view(), name='post-create'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
]
