from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, View

from .user_forms import DashboardUserCreateForm, DashboardUserForm, GroupForm

User = get_user_model()


class StaffRequiredMixin:
    """تأییدشده + staff یا superuser — قبل از اجرای ویو چک می‌شود."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_active:
            return redirect('accounts:login')
        if not getattr(request.user, 'is_approved', False):
            return redirect('accounts:pending')
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'دسترسی به این بخش فقط برای مدیران است.')
            return redirect('dashboard:index')
        return super().dispatch(request, *args, **kwargs)


class SuperuserRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_active or not getattr(request.user, 'is_approved', False):
            return redirect('accounts:pending')
        if not request.user.is_superuser:
            messages.error(request, 'فقط مدیر کل به این بخش دسترسی دارد.')
            return redirect('dashboard:index')
        return super().dispatch(request, *args, **kwargs)


def _permissions_by_app():
    perms = Permission.objects.select_related('content_type').order_by(
        'content_type__app_label', 'codename'
    )
    grouped = {}
    for p in perms:
        key = f'{p.content_type.app_label}.{p.content_type.model}'
        grouped.setdefault(key, []).append(p)
    return grouped


@method_decorator(login_required, name='dispatch')
class UserListView(StaffRequiredMixin, ListView):
    model = User
    template_name = 'dashboard/users/user_list.html'
    context_object_name = 'users'
    paginate_by = 25

    def get_queryset(self):
        qs = User.objects.all().prefetch_related('groups').order_by('-created_at')
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(phone_number__icontains=q)
                | Q(first_name__icontains=q)
                | Q(last_name__icontains=q)
                | Q(email__icontains=q)
                | Q(job_title__icontains=q)
            )
        status = self.request.GET.get('status')
        if status in ('pending', 'approved', 'rejected'):
            qs = qs.filter(approval_status=status)
        role = self.request.GET.get('role')
        if role == 'staff':
            qs = qs.filter(is_staff=True)
        elif role == 'superuser':
            qs = qs.filter(is_superuser=True)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        base = User.objects.all()
        ctx['count_all'] = base.count()
        ctx['count_pending'] = base.filter(approval_status='pending').count()
        ctx['count_approved'] = base.filter(approval_status='approved').count()
        ctx['count_rejected'] = base.filter(approval_status='rejected').count()
        return ctx


@method_decorator(login_required, name='dispatch')
class UserCreateView(StaffRequiredMixin, CreateView):
    model = User
    form_class = DashboardUserCreateForm
    template_name = 'dashboard/users/user_form.html'
    success_url = reverse_lazy('dashboard:user_list')

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['request_user'] = self.request.user
        return kw

    def form_valid(self, form):
        messages.success(self.request, 'کاربر ایجاد شد.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'ایجاد کاربر'
        ctx['submit_label'] = 'ایجاد'
        return ctx


@method_decorator(login_required, name='dispatch')
class UserUpdateView(StaffRequiredMixin, UpdateView):
    model = User
    form_class = DashboardUserForm
    template_name = 'dashboard/users/user_form.html'
    success_url = reverse_lazy('dashboard:user_list')
    pk_url_kwarg = 'pk'

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['request_user'] = self.request.user
        return kw

    def form_valid(self, form):
        if self.object.pk == self.request.user.pk:
            form.instance.is_active = True
            if self.request.user.is_superuser:
                form.instance.is_superuser = True
                form.instance.is_staff = True
        messages.success(self.request, 'اطلاعات کاربر ذخیره شد.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = f'ویرایش — {self.object}'
        ctx['submit_label'] = 'ذخیره'
        return ctx


@method_decorator(login_required, name='dispatch')
class UserApproveView(StaffRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        action = request.POST.get('action')
        if action == 'approve':
            user.approve(by_user=request.user)
            messages.success(request, f'«{user}» تأیید شد.')
        elif action == 'reject':
            reason = request.POST.get('reason', 'رد از پنل داشبورد')
            user.reject(by_user=request.user, reason=reason)
            messages.warning(request, f'«{user}» رد شد.')
        return redirect(request.POST.get('next') or 'dashboard:user_list')


@method_decorator(login_required, name='dispatch')
class GroupListView(StaffRequiredMixin, ListView):
    model = Group
    template_name = 'dashboard/users/group_list.html'
    context_object_name = 'groups'

    def get_queryset(self):
        return Group.objects.annotate(
            user_count=Count('user'),
            perm_count=Count('permissions'),
        ).order_by('name')


@method_decorator(login_required, name='dispatch')
class GroupCreateView(SuperuserRequiredMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'dashboard/users/group_form.html'
    success_url = reverse_lazy('dashboard:group_list')

    def form_valid(self, form):
        messages.success(self.request, 'گروه ایجاد شد.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'ایجاد گروه'
        ctx['submit_label'] = 'ایجاد گروه'
        ctx['perm_groups'] = _permissions_by_app()
        return ctx


@method_decorator(login_required, name='dispatch')
class GroupUpdateView(SuperuserRequiredMixin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'dashboard/users/group_form.html'
    success_url = reverse_lazy('dashboard:group_list')

    def form_valid(self, form):
        messages.success(self.request, 'گروه به‌روز شد.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = f'ویرایش گروه — {self.object.name}'
        ctx['submit_label'] = 'ذخیره'
        ctx['perm_groups'] = _permissions_by_app()
        return ctx


@method_decorator(login_required, name='dispatch')
class GroupDeleteView(SuperuserRequiredMixin, DeleteView):
    model = Group
    template_name = 'dashboard/users/group_confirm_delete.html'
    success_url = reverse_lazy('dashboard:group_list')

    def form_valid(self, form):
        messages.success(self.request, 'گروه حذف شد.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class PermissionListView(StaffRequiredMixin, ListView):
    model = Permission
    template_name = 'dashboard/users/permission_list.html'
    context_object_name = 'permissions'

    def get_queryset(self):
        return Permission.objects.select_related('content_type').order_by(
            'content_type__app_label', 'content_type__model', 'codename'
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['perm_groups'] = _permissions_by_app()
        return ctx
