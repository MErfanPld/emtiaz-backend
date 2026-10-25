from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from blog.models import Category, Post, Tag

from .blog_forms import CategoryForm, PostForm, TagForm
from .views import StaffManagerMixin


@method_decorator(login_required, name='dispatch')
class BlogPostListView(StaffManagerMixin, ListView):
    model = Post
    template_name = 'dashboard/blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_queryset(self):
        qs = Post.objects.select_related('category').prefetch_related('tags').order_by('-created_at')
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(title_en__icontains=q) | Q(excerpt__icontains=q))
        status = self.request.GET.get('status')
        if status == 'published':
            qs = qs.filter(is_published=True)
        elif status == 'draft':
            qs = qs.filter(is_published=False)
        return qs


@method_decorator(login_required, name='dispatch')
class BlogPostCreateView(StaffManagerMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'dashboard/blog/post_form.html'
    success_url = reverse_lazy('dashboard:blog_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'مقاله ذخیره شد.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'مقاله جدید'
        ctx['submit_label'] = 'ثبت مقاله'
        return ctx


@method_decorator(login_required, name='dispatch')
class BlogPostUpdateView(StaffManagerMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'dashboard/blog/post_form.html'
    success_url = reverse_lazy('dashboard:blog_list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        messages.success(self.request, 'مقاله به‌روز شد.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = f'ویرایش — {self.object.title[:40]}'
        ctx['submit_label'] = 'ذخیره'
        return ctx


@method_decorator(login_required, name='dispatch')
class BlogPostDeleteView(StaffManagerMixin, DeleteView):
    model = Post
    template_name = 'dashboard/blog/post_confirm_delete.html'
    success_url = reverse_lazy('dashboard:blog_list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        messages.success(self.request, 'مقاله حذف شد.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class BlogCategoryListView(StaffManagerMixin, ListView):
    model = Category
    template_name = 'dashboard/blog/category_list.html'
    context_object_name = 'categories'


@method_decorator(login_required, name='dispatch')
class BlogCategoryCreateView(StaffManagerMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'dashboard/blog/category_form.html'
    success_url = reverse_lazy('dashboard:blog_category_list')

    def form_valid(self, form):
        messages.success(self.request, 'دسته ایجاد شد.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'دسته جدید'
        return ctx


@method_decorator(login_required, name='dispatch')
class BlogCategoryUpdateView(StaffManagerMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'dashboard/blog/category_form.html'
    success_url = reverse_lazy('dashboard:blog_category_list')

    def form_valid(self, form):
        messages.success(self.request, 'دسته به‌روز شد.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = f'ویرایش — {self.object.name}'
        return ctx


@method_decorator(login_required, name='dispatch')
class BlogCategoryDeleteView(StaffManagerMixin, DeleteView):
    model = Category
    template_name = 'dashboard/blog/category_confirm_delete.html'
    success_url = reverse_lazy('dashboard:blog_category_list')

    def form_valid(self, form):
        messages.success(self.request, 'دسته حذف شد.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class BlogTagListView(StaffManagerMixin, ListView):
    model = Tag
    template_name = 'dashboard/blog/tag_list.html'
    context_object_name = 'tags'


@method_decorator(login_required, name='dispatch')
class BlogTagCreateView(StaffManagerMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'dashboard/blog/tag_form.html'
    success_url = reverse_lazy('dashboard:blog_tag_list')

    def form_valid(self, form):
        messages.success(self.request, 'برچسب ایجاد شد.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'برچسب جدید'
        return ctx


@method_decorator(login_required, name='dispatch')
class BlogTagUpdateView(StaffManagerMixin, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = 'dashboard/blog/tag_form.html'
    success_url = reverse_lazy('dashboard:blog_tag_list')

    def form_valid(self, form):
        messages.success(self.request, 'برچسب به‌روز شد.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = f'ویرایش — {self.object.name}'
        return ctx


@method_decorator(login_required, name='dispatch')
class BlogTagDeleteView(StaffManagerMixin, DeleteView):
    model = Tag
    template_name = 'dashboard/blog/tag_confirm_delete.html'
    success_url = reverse_lazy('dashboard:blog_tag_list')

    def form_valid(self, form):
        messages.success(self.request, 'برچسب حذف شد.')
        return super().form_valid(form)
