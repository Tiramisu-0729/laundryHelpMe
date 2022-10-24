from django import forms
from .models import Cabinet

class JudgeForm(forms.ModelForm):
    class Meta:
        model = Cabinet
        fields = ['image']

class CabinetForm(forms.ModelForm):
    class Meta:
        model = Cabinet
        fields = ['image', 'category', 'memo']