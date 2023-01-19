from django import forms
from .models import Cabinet,Profile,User
from django.contrib.auth.forms import PasswordChangeForm

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

class CabinetCategoryFrom(forms.ModelForm):
    class Meta:
        model = Cabinet
        fields = ['category']

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


class MyPasswordChangeForm(PasswordChangeForm):

    # テンプレートにおいて表示されるinputタグのカスタマイズは以下のように行う（下は一例）
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = 'old'# classの指定
        self.fields['new_password1'].widget.attrs['class'] = 'new'
        self.fields['new_password2'].widget.attrs['class'] = 're'
        self.fields['new_password1'].widget.attrs['placeholder'] = '半角英数字８文字以上'# placeholderの指定
        self.fields['new_password2'].widget.attrs['placeholder'] = 'パスワード確認用'