from django.contrib import admin

from .models import Category, Post, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_en', 'slug', 'sort_order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('sort_order', 'is_active')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_en', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_published', 'is_featured', 'published_at', 'views_count')
    list_filter = ('is_published', 'is_featured', 'category', 'tags')
    search_fields = ('title', 'title_en', 'excerpt', 'body')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    list_editable = ('is_published', 'is_featured')
    date_hierarchy = 'published_at'
    readonly_fields = ('views_count', 'created_at', 'updated_at')
