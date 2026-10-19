from django.urls import path

from .views import (
    DashboardIndexView,
    PropertyCreateView,
    PropertyDashboardListView,
    PropertyDeleteView,
    PropertyUpdateView,
)

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardIndexView.as_view(), name='index'),
    path('properties/', PropertyDashboardListView.as_view(), name='property_list'),
    path('properties/new/', PropertyCreateView.as_view(), name='property_create'),
    path('properties/<slug:slug>/edit/', PropertyUpdateView.as_view(), name='property_edit'),
    path('properties/<slug:slug>/delete/', PropertyDeleteView.as_view(), name='property_delete'),
]
