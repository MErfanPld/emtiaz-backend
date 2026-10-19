from django import forms

from .models import ConsultationRequest

CSS = (
    'w-full h-11 bg-surface text-on-surface text-body-md font-body-md '
    'rounded-lg border border-outline-variant/60 px-3 focus:outline-none '
    'focus:ring-2 focus:ring-secondary/40 focus:border-primary'
)


class ConsultationForm(forms.ModelForm):
    class Meta:
        model = ConsultationRequest
        fields = ['full_name', 'phone', 'request_type', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': CSS,
                'placeholder': 'مثال: علی رضایی',
                'required': True,
            }),
            'phone': forms.TextInput(attrs={
                'class': CSS + ' font-mono text-left',
                'placeholder': '۰۹۱۲...',
                'dir': 'ltr',
                'type': 'tel',
                'required': True,
            }),
            'request_type': forms.Select(attrs={'class': CSS}),
            'message': forms.Textarea(attrs={
                'class': CSS.replace('h-11', 'min-h-[80px]'),
                'rows': 2,
                'placeholder': 'توضیح کوتاه (اختیاری)',
            }),
        }

    def clean_phone(self):
        phone = (self.cleaned_data.get('phone') or '').strip().replace(' ', '').replace('-', '')
        trans = str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789')
        phone = phone.translate(trans)
        if phone.startswith('+98'):
            phone = '0' + phone[3:]
        if phone.startswith('98') and len(phone) >= 12:
            phone = '0' + phone[2:]
        if not phone.isdigit() or len(phone) < 10:
            raise forms.ValidationError('شماره تماس معتبر وارد کنید.')
        return phone
