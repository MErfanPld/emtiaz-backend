from django.contrib import admin

from .models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'title',
        'transaction_type',
        'property_type',
        'area_name',
        'area_sqm',
        'price',
        'agency_name',
        'is_active',
        'is_featured',
        'created_at',
    )
    list_filter = (
        'transaction_type',
        'property_type',
        'is_active',
        'is_featured',
        'is_exclusive',
        'has_deed',
        'is_complex_office',
    )
    search_fields = ('code', 'title', 'title_en', 'area_name', 'agency_name', 'address_line')
    list_editable = ('is_active', 'is_featured')
    prepopulated_fields = {'slug': ('title_en', 'code')}
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    save_on_top = True

    fieldsets = (
        ('شناسه و عنوان', {
            'fields': ('code', 'title', 'title_en', 'slug'),
        }),
        ('نوع و موقعیت', {
            'fields': (
                'transaction_type',
                'property_type',
                'area_name',
                'area_name_en',
                'address_line',
                'address_line_en',
            ),
        }),
        ('مشخصات فنی', {
            'fields': ('area_sqm', 'bedrooms', 'parking', 'floor'),
        }),
        ('قیمت', {
            'fields': ('price', 'price_label'),
        }),
        ('دفتر و نشان‌ها', {
            'fields': ('agency_name', 'agency_name_en', 'badge_primary', 'badge_secondary'),
        }),
        ('تصاویر', {
            'fields': ('cover_image', 'cover_image_url', 'image_count'),
        }),
        ('فیلترهای اعتباری', {
            'fields': (
                'has_deed',
                'is_complex_office',
                'has_pool_or_roof',
                'is_brand_builder',
                'is_exclusive',
            ),
        }),
        ('وضعیت نمایش', {
            'fields': ('is_active', 'is_featured', 'sort_order'),
        }),
        ('توضیحات', {
            'fields': ('description', 'description_en'),
            'classes': ('collapse',),
        }),
        ('زمان‌ها', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
