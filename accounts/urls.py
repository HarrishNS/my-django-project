from django.urls import path
from .views import follow_user, unfollow_user, get_follow_data

urlpatterns = [
    path('follow/', follow_user, name='follow-user'),
    path('unfollow/', unfollow_user, name='unfollow-user'),
    path('follow-data/<int:user_id>/', get_follow_data, name='follow-data'),
]
