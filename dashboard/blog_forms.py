from django import forms

from blog.models import Category, Post, Tag

CSS = 'w-full border border-[#c1c8c4] rounded-lg px-3 py-2 text-sm bg-white'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'name_en', 'slug', 'sort_order', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'is_active':
                field.widget.attrs['class'] = 'rounded'
            else:
                field.widget.attrs['class'] = CSS


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'name_en', 'slug', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'is_active':
                field.widget.attrs['class'] = 'rounded'
            else:
                field.widget.attrs['class'] = CSS


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title', 'title_en', 'slug', 'category', 'tags',
            'excerpt', 'excerpt_en', 'body', 'body_en',
            'cover_image', 'cover_image_url',
            'author_name', 'author_name_en', 'reading_minutes',
            'is_published', 'is_featured', 'published_at',
        ]
        widgets = {
            'excerpt': forms.Textarea(attrs={'rows': 3}),
            'excerpt_en': forms.Textarea(attrs={'rows': 3}),
            'published_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'tags': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['published_at'].input_formats = ['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M']
        self.fields['tags'].queryset = Tag.objects.filter(is_active=True)
        for name, field in self.fields.items():
            if name in ('is_published', 'is_featured', 'tags'):
                if name != 'tags':
                    field.widget.attrs['class'] = 'rounded'
                continue
            if name in ('cover_image', 'body', 'body_en'):
                continue
            field.widget.attrs.setdefault('class', CSS)
