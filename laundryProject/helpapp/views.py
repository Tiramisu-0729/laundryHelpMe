from unicodedata import category

from django.test import tag
from .models import Cabinet, Categories
from django.shortcuts import redirect, render, get_object_or_404
from .forms import CabinetForm, JudgeForm

def helpapp(request):
    #ログインがあるか判別
    if request.user.is_authenticated :
        return home(request)
    else :
        return render(request, 'helpapp/index.html')

def register(request):
    return render(request, 'helpapp/register.html')

def nologin(request):
    return render(request, 'helpapp/nologin.html')

def home(request):
    user = request.user
    context = {
        'message': 'Judage',
        'user': user,
        'form': JudgeForm(),
    }
    return render(request, 'home/index.html', context)
    
def washing_machine(request):
    context = {
        'message': 'Laundry',
    }
    return render(request, 'washing_machine/index.html',context)

def cabinet(request):
    user = request.user
    cabinets = Cabinet.objects.filter(author=user)
    context = {
        'message': 'Cabinet',
        'cabinets' : cabinets,
        'user' : user,
    }
    return render(request, 'cabinet/index.html', context)

def cabinet_form(request):
    user = request.user
    context = {
        'message': 'Add Cabinet',
        'user': user,
        'cabinet_form': CabinetForm(),
    }
    return render(request, 'cabinet/add.html', context)

def cabinet_add(request):
    if request.method == "POST":
        form = CabinetForm(request.POST)
        if form.is_valid():#formの内容が正しければ
            cabinet = Cabinet()
            print(request)
            cabinet.author = request.user
            cabinet.category = Categories(request.POST['category'])#category型じゃないと怒られた
            cabinet.laundry_tag = "aaaaaaaaa"#判定結果
            cabinet.image = request.FILES['image']#保存先はupload_img＞upload_img>imgのなか
            cabinet.save()
            context = {
                'message': 'Success',
            }
        return render(request, 'cabinet/index.html', context)
    else:
        user = request.user
        context = {
            'message': 'Error',
            'user': user,
            'cabinet_form': CabinetForm(),
        }
    return render(request, 'cabinet/add.html', context)

def cabinet_detail(request, pk):
    cabinet = Cabinet.objects.get(pk=pk)
    context = {
        'message': 'Error',
        'cabinet' : cabinet,
    }
    return render(request, 'cabinet/detail.html', context)
    
def user(request):
    user = request.user
    context = {
        'message': 'User',
        'user': user,
    }
    return render(request, 'user/index.html', context)

def timeline(request):
    tag_list = ['LA','B3', 'T2', 'N6', 'D3', 'W4']

    context = {
        'tag': tag_list,
    }
    return render(request, 'timeline/index.html', context)

def judge(request):
    # if (request.method == 'POST'):
        # upload_image = cabinet(image=request.POST, request.FILES['image']) 画像だけとりたいpath入らない
    return render(request, 'washing_machine.html')
