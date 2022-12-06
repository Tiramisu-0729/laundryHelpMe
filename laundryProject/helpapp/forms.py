from django import forms
from .models import Cabinet,Profile

class JudgeForm(forms.Form):
    UploadImg = forms.FileField()

class CabinetForm(forms.ModelForm):
    class Meta:
        model = Cabinet
        fields = ['image','name' ,'category', 'memo']
        widgets = {
            'memo': forms.Textarea
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']