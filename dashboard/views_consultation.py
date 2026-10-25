from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, ListView

from core.models import ConsultationRequest

from .views import StaffManagerMixin


@method_decorator(login_required, name='dispatch')
class ConsultationListView(StaffManagerMixin, ListView):
    model = ConsultationRequest
    template_name = 'dashboard/consultation/list.html'
    context_object_name = 'items'
    paginate_by = 25

    def get_queryset(self):
        qs = ConsultationRequest.objects.all()
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(Q(full_name__icontains=q) | Q(phone__icontains=q))
        status = self.request.GET.get('status')
        if status in dict(ConsultationRequest.Status.choices):
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        base = ConsultationRequest.objects.all()
        ctx['count_new'] = base.filter(status='new').count()
        ctx['count_all'] = base.count()
        return ctx


@method_decorator(login_required, name='dispatch')
class ConsultationDetailView(StaffManagerMixin, DetailView):
    model = ConsultationRequest
    template_name = 'dashboard/consultation/detail.html'
    context_object_name = 'item'


@method_decorator(login_required, name='dispatch')
class ConsultationStatusView(StaffManagerMixin, View):
    def post(self, request, pk):
        item = get_object_or_404(ConsultationRequest, pk=pk)
        status = request.POST.get('status')
        note = request.POST.get('admin_note', '').strip()
        if status in dict(ConsultationRequest.Status.choices):
            item.status = status
        if note:
            item.admin_note = note
        item.save()
        messages.success(request, 'وضعیت درخواست به‌روز شد.')
        return redirect(request.POST.get('next') or reverse_lazy('dashboard:consultation_list'))
