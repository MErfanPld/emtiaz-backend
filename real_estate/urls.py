from django.urls import path

from .views import PropertyListView

app_name = 'real_estate'

urlpatterns = [
    path('', PropertyListView.as_view(), name='list'),
]
