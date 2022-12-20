from django import forms
from .models import Cabinet,Profile,User

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

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control' }))

    class Meta:
        model = User
        fields = ['username']


class UpdateProfileForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    
    class Meta:
        model = Profile
        fields = ['image']