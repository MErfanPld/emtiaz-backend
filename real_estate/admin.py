from django.contrib import admin

from .models import Property, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3
    fields = ('image', 'image_url', 'caption', 'caption_en', 'sort_order')
    ordering = ('sort_order', 'id')
    fk_name = 'listing'


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
    inlines = [PropertyImageInline]

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
            'fields': (
                'area_sqm',
                'bedrooms',
                'parking',
                'floor',
                'floor_en',
                'year_built',
                'year_built_en',
            ),
        }),
        ('قیمت', {
            'fields': ('price', 'price_label', 'price_label_en'),
        }),
        ('دفتر و مشاور', {
            'fields': (
                'agency_name',
                'agency_name_en',
                'consultant_name',
                'consultant_name_en',
                'consultant_phone',
                'badge_primary',
                'badge_primary_en',
                'badge_secondary',
                'badge_secondary_en',
            ),
        }),
        ('تصویر کاور', {
            'fields': ('cover_image', 'cover_image_url', 'image_count'),
            'description': 'گالری چندتصویری را از بخش «تصاویر ملک» پایین فرم اضافه کنید.',
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
        }),
        ('زمان‌ها', {
            'fields': ('created_at', 'updated_at'),
        }),
    )


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('listing', 'caption', 'sort_order', 'image', 'image_url')
    list_filter = ('listing',)
    search_fields = ('listing__code', 'caption', 'caption_en')
    ordering = ('listing', 'sort_order')
