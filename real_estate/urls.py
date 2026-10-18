from django.urls import path

from .views import PropertyDetailView, PropertyListView

app_name = 'real_estate'

urlpatterns = [
    path('', PropertyListView.as_view(), name='list'),
    path('<slug:slug>/', PropertyDetailView.as_view(), name='detail'),
]
