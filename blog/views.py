import re
from html import unescape

from django.db.models import F, Q
from django.utils.translation import get_language
from django.views.generic import DetailView, ListView

from .models import Category, Post, Tag


def _lang_is_en():
    return (get_language() or 'fa')[:2] == 'en'


def _build_toc_and_body(html: str):
    """Extract h2/h3 headings, inject id attributes, return (toc_list, modified_html)."""
    if not html:
        return [], html or ''

    toc = []
    counter = [0]

    def replacer(match):
        tag = match.group(1).lower()
        attrs = match.group(2) or ''
        inner = match.group(3)
        text = unescape(re.sub(r'<[^>]+>', '', inner)).strip()
        if not text:
            return match.group(0)
        counter[0] += 1
        sid = f'section-{counter[0]}'
        # keep existing id if present
        if re.search(r'\bid\s*=', attrs, re.I):
            sid_match = re.search(r'\bid\s*=\s*["\']([^"\']+)["\']', attrs, re.I)
            if sid_match:
                sid = sid_match.group(1)
            toc.append({'id': sid, 'text': text, 'level': tag})
            return match.group(0)
        toc.append({'id': sid, 'text': text, 'level': tag})
        return f'<{tag} id="{sid}"{attrs}>{inner}</{tag}>'

    modified = re.sub(
        r'<(h[23])(\s[^>]*)?>(.*?)</\1>',
        replacer,
        html,
        flags=re.I | re.S,
    )
    return toc, modified


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 9

    def get_template_names(self):
        if _lang_is_en():
            return ['blog/post_list_en.html']
        return ['blog/post_list.html']

    def get_queryset(self):
        qs = Post.objects.filter(is_published=True).select_related('category').prefetch_related('tags')
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(title__icontains=q)
                | Q(title_en__icontains=q)
                | Q(excerpt__icontains=q)
                | Q(excerpt_en__icontains=q)
                | Q(body__icontains=q)
                | Q(tags__name__icontains=q)
                | Q(tags__name_en__icontains=q)
            ).distinct()
        cat = self.request.GET.get('category', '').strip()
        if cat:
            qs = qs.filter(category__slug=cat)
        tag = self.request.GET.get('tag', '').strip()
        if tag:
            qs = qs.filter(tags__slug=tag)
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
        ctx['tags'] = Tag.objects.filter(is_active=True)
        ctx['active_category'] = self.request.GET.get('category', '')
        ctx['active_tag'] = self.request.GET.get('tag', '')
        ctx['q'] = self.request.GET.get('q', '')
        ctx['sort'] = self.request.GET.get('sort', 'newest')
        ctx['is_en'] = _lang_is_en()
        return ctx


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_template_names(self):
        if _lang_is_en():
            return ['blog/post_detail_en.html']
        return ['blog/post_detail.html']

    def get_queryset(self):
        return Post.objects.filter(is_published=True).select_related('category').prefetch_related('tags')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        Post.objects.filter(pk=obj.pk).update(views_count=F('views_count') + 1)
        obj.refresh_from_db(fields=['views_count'])
        return obj

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        post = self.object
        is_en = _lang_is_en()
        raw_body = post.display_body() if is_en else post.body
        toc, body_html = _build_toc_and_body(raw_body or '')
        ctx['toc'] = toc
        ctx['body_html'] = body_html
        related = (
            Post.objects.filter(is_published=True)
            .exclude(pk=post.pk)
            .select_related('category')
            .prefetch_related('tags')
        )
        if post.category_id:
            related = related.filter(category_id=post.category_id) | related
        ctx['related_posts'] = related.distinct().order_by('-published_at')[:3]
        ctx['is_en'] = is_en
        return ctx
