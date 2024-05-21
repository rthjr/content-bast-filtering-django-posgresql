from django.urls import path
from .views import search
from .views import goal_list

urlpatterns = [
    path('', search, name="search"),
    path('goal/', goal_list, name='goal-list'),
]
