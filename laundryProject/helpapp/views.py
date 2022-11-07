from distutils.command.upload import upload
import os
from unicodedata import category

from django.test import tag
from unittest import result
from .models import Cabinet, Categories
from django.shortcuts import redirect, render, get_object_or_404
from .forms import CabinetForm, JudgeForm
from django.core.files.storage import FileSystemStorage

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
        'message': cabinet.name,
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
    if request.method == "POST":
        image = request.FILES['UploadImg']#保存先はupload_img＞upload_img>imgのなか
        fs = FileSystemStorage()
        file_data = fs.save(image.name, image)
        file_url = fs.url(file_data)
        print(file_url)
        #AIで画像判定
        #text 解析
        result = "L8,B3,T3,N1,I4"#ここに結果を入れる
        tag_list = result.split(',') 
        context = {
            'file_url' : file_url,
            'message': 'result',
            'tag_list': tag_list
        }
        return render(request, 'laundry_tag_check/index.html', context)
    else:
        user = request.user
        context = {
            'message': 'Error',
            'user': user,
            'form': JudgeForm(),
        }
    return render(request, 'home/index.html', context)
    
def judge_result(request):
     #継承するfile_url = judge.file_url
    #画像消す

    return render(request, 'home/index.html')