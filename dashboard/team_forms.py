from django import forms

from core.models import TeamMember

CSS_INPUT = (
    'w-full border border-[#c1c8c4] rounded-lg px-3 py-2 text-sm '
    'bg-white focus:outline-none focus:border-primary'
)


class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = [
            'role', 'department',
            'name', 'name_en',
            'title', 'title_en',
            'bio', 'bio_en',
            'photo', 'photo_url',
            'is_active', 'sort_order',
        ]
        widgets = {
            'role': forms.Select(attrs={'class': CSS_INPUT}),
            'department': forms.Select(attrs={'class': CSS_INPUT}),
            'name': forms.TextInput(attrs={'class': CSS_INPUT}),
            'name_en': forms.TextInput(attrs={'class': CSS_INPUT}),
            'title': forms.TextInput(attrs={'class': CSS_INPUT}),
            'title_en': forms.TextInput(attrs={'class': CSS_INPUT}),
            'bio': forms.Textarea(attrs={'class': CSS_INPUT, 'rows': 3}),
            'bio_en': forms.Textarea(attrs={'class': CSS_INPUT, 'rows': 3}),
            'photo_url': forms.URLInput(attrs={
                'class': CSS_INPUT,
                'placeholder': 'https://...',
            }),
            'photo': forms.ClearableFileInput(attrs={'class': 'text-sm'}),
            'sort_order': forms.NumberInput(attrs={
                'class': CSS_INPUT,
                'min': 0,
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded text-primary'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sort_order'].required = False
        self.fields['department'].required = False
        self.fields['photo'].required = False
        self.fields['photo_url'].required = False
