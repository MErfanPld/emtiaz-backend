from django.db.models import F, Q
from django.views.generic import DetailView, ListView

from .models import Category, Post


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        qs = Post.objects.filter(is_published=True).select_related('category')
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(title__icontains=q)
                | Q(excerpt__icontains=q)
                | Q(body__icontains=q)
                | Q(tags__icontains=q)
            )
        cat = self.request.GET.get('category', '').strip()
        if cat:
            qs = qs.filter(category__slug=cat)
        sort = self.request.GET.get('sort', 'newest')
        if sort == 'views':
            qs = qs.order_by('-views_count', '-published_at')
        elif sort == 'featured':
            qs = qs.order_by('-is_featured', '-published_at')
        else:
            qs = qs.order_by('-published_at', '-created_at')
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.filter(is_active=True)
        ctx['active_category'] = self.request.GET.get('category', '')
        ctx['q'] = self.request.GET.get('q', '')
        ctx['sort'] = self.request.GET.get('sort', 'newest')
        return ctx


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Post.objects.filter(is_published=True).select_related('category')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        Post.objects.filter(pk=obj.pk).update(views_count=F('views_count') + 1)
        obj.refresh_from_db(fields=['views_count'])
        return obj

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        post = self.object
        related = (
            Post.objects.filter(is_published=True)
            .exclude(pk=post.pk)
            .select_related('category')
        )
        if post.category_id:
            related = related.filter(category_id=post.category_id) | related
        ctx['related_posts'] = related.distinct().order_by('-published_at')[:3]
        return ctx
