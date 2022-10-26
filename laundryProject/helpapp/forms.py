from django import forms
from .models import Cabinet

class JudgeForm(forms.Form):
    UploadImg = forms.FileField()

class CabinetForm(forms.ModelForm):
    class Meta:
        model = Cabinet
        fields = ['image', 'category', 'memo']