from django import forms

from blog.models import Category, Post

CSS = 'w-full border border-[#c1c8c4] rounded-lg px-3 py-2 text-sm bg-white'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'sort_order', 'is_active']

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
            'title', 'slug', 'category', 'excerpt', 'body',
            'cover_image', 'cover_image_url',
            'author_name', 'reading_minutes', 'tags',
            'is_published', 'is_featured', 'published_at',
        ]
        widgets = {
            'excerpt': forms.Textarea(attrs={'rows': 3}),
            'body': forms.Textarea(attrs={'rows': 14}),
            'published_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['published_at'].input_formats = ['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M']
        for name, field in self.fields.items():
            if name in ('is_published', 'is_featured'):
                field.widget.attrs['class'] = 'rounded'
            elif name == 'cover_image':
                field.widget.attrs['class'] = 'text-sm'
            else:
                field.widget.attrs.setdefault('class', CSS)
