from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from core.models import TeamMember

from .team_forms import TeamMemberForm
from .views_users import StaffRequiredMixin


@method_decorator(login_required, name='dispatch')
class TeamMemberListView(StaffRequiredMixin, ListView):
    model = TeamMember
    template_name = 'dashboard/team/list.html'
    context_object_name = 'members'
    paginate_by = 30

    def get_queryset(self):
        qs = TeamMember.objects.all().order_by('sort_order', 'role', 'id')
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(name__icontains=q)
                | Q(name_en__icontains=q)
                | Q(title__icontains=q)
            )
        role = self.request.GET.get('role')
        if role in dict(TeamMember.Role.choices):
            qs = qs.filter(role=role)
        active = self.request.GET.get('active')
        if active == '1':
            qs = qs.filter(is_active=True)
        elif active == '0':
            qs = qs.filter(is_active=False)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['role_choices'] = TeamMember.Role.choices
        return ctx


@method_decorator(login_required, name='dispatch')
class TeamMemberCreateView(StaffRequiredMixin, CreateView):
    model = TeamMember
    form_class = TeamMemberForm
    template_name = 'dashboard/team/form.html'
    success_url = reverse_lazy('dashboard:team_list')

    def form_valid(self, form):
        messages.success(self.request, 'عضو تیم اضافه شد.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'افزودن عضو تیم'
        ctx['submit_label'] = 'ثبت'
        return ctx


@method_decorator(login_required, name='dispatch')
class TeamMemberUpdateView(StaffRequiredMixin, UpdateView):
    model = TeamMember
    form_class = TeamMemberForm
    template_name = 'dashboard/team/form.html'
    success_url = reverse_lazy('dashboard:team_list')
    pk_url_kwarg = 'pk'

    def form_valid(self, form):
        messages.success(self.request, 'اطلاعات عضو تیم ذخیره شد.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = f'ویرایش — {self.object.name}'
        ctx['submit_label'] = 'ذخیره'
        return ctx


@method_decorator(login_required, name='dispatch')
class TeamMemberDeleteView(StaffRequiredMixin, DeleteView):
    model = TeamMember
    template_name = 'dashboard/team/confirm_delete.html'
    success_url = reverse_lazy('dashboard:team_list')
    pk_url_kwarg = 'pk'

    def form_valid(self, form):
        messages.success(self.request, 'عضو تیم حذف شد.')
        return super().form_valid(form)
