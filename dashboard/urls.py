from django.urls import path

from .views import (
    DashboardIndexView,
    PropertyCreateView,
    PropertyDashboardListView,
    PropertyDeleteView,
    PropertyUpdateView,
)
from .views_blog import (
    BlogCategoryCreateView,
    BlogCategoryDeleteView,
    BlogCategoryListView,
    BlogCategoryUpdateView,
    BlogPostCreateView,
    BlogPostDeleteView,
    BlogPostListView,
    BlogPostUpdateView,
)
from .views_users import (
    GroupCreateView,
    GroupDeleteView,
    GroupListView,
    GroupUpdateView,
    PermissionListView,
    UserApproveView,
    UserCreateView,
    UserListView,
    UserUpdateView,
)

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardIndexView.as_view(), name='index'),
    # املاک
    path('properties/', PropertyDashboardListView.as_view(), name='property_list'),
    path('properties/new/', PropertyCreateView.as_view(), name='property_create'),
    path('properties/<slug:slug>/edit/', PropertyUpdateView.as_view(), name='property_edit'),
    path('properties/<slug:slug>/delete/', PropertyDeleteView.as_view(), name='property_delete'),
    # وبلاگ
    path('blog/', BlogPostListView.as_view(), name='blog_list'),
    path('blog/new/', BlogPostCreateView.as_view(), name='blog_create'),
    path('blog/<slug:slug>/edit/', BlogPostUpdateView.as_view(), name='blog_edit'),
    path('blog/<slug:slug>/delete/', BlogPostDeleteView.as_view(), name='blog_delete'),
    path('blog/categories/', BlogCategoryListView.as_view(), name='blog_category_list'),
    path('blog/categories/new/', BlogCategoryCreateView.as_view(), name='blog_category_create'),
    path('blog/categories/<int:pk>/edit/', BlogCategoryUpdateView.as_view(), name='blog_category_edit'),
    path('blog/categories/<int:pk>/delete/', BlogCategoryDeleteView.as_view(), name='blog_category_delete'),
    # کاربران و دسترسی
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/new/', UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/edit/', UserUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/approve/', UserApproveView.as_view(), name='user_approve'),
    path('groups/', GroupListView.as_view(), name='group_list'),
    path('groups/new/', GroupCreateView.as_view(), name='group_create'),
    path('groups/<int:pk>/edit/', GroupUpdateView.as_view(), name='group_edit'),
    path('groups/<int:pk>/delete/', GroupDeleteView.as_view(), name='group_delete'),
    path('permissions/', PermissionListView.as_view(), name='permission_list'),
]
