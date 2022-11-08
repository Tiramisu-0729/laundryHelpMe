from distutils.command.upload import upload
import json
import os
import pandas as pd
from django.urls import reverse
from urllib.parse import urlencode
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
            cabinet.name = request.POST['name']
            cabinet.memo = request.POST['memo']
            cabinet.category = Categories(request.POST['category'])#category型じゃないと怒られた
            cabinet.laundry_tag = request.POST['laundry_tag']#判定結果
            cabinet.image = request.FILES['image']#保存先はupload_img＞upload_img>imgのなか
            cabinet.save()
            context = {
                'message': 'Cabinet',
                'i':1,
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
    user = request.user
    cabinets = Cabinet.objects.filter(author=user).order_by('-id')
    cnt = 0
    TimeLineCab = []
    tag_list = []
    for cab in cabinets :
        if 10 < cnt:
            break
        cab.laundry_tag = cab.laundry_tag.split(',')
        cnt += 1
        TimeLineCab.append(cab)
    context = {
        'tag_list': tag_list,
        'message': 'TimeLine',
        'cabinets' : TimeLineCab,
    }
    return render(request, 'timeline/index.html', context)

def judge(request):
    if request.method == "POST":
        image = request.FILES['UploadImg']#保存先はupload_imgのなか　いったん保存
        fs = FileSystemStorage()
        file_data = fs.save(image.name, image)
        file_url = fs.url(file_data)
        #AIで画像判定
        #判定結果 解析
        result = "L8,B3,T3,N1,I4"#ここに結果を入れる
        result = result.split(',') 
        redirect_url = reverse('helpapp:laundry_tag_check')
        parameters = urlencode({'file_url': file_url, 'result' : result})
        url = f'{redirect_url}?{parameters}'
        return redirect(url)
    else:
        user = request.user
        context = {
            'message': 'judge',
            'user': user,
            'form': JudgeForm(),
        }
    return render(request, 'home/index.html', context)

def laundry_tag_check(request):
    file_url = request.GET.get('file_url') # param1の値を取得
    results = request.GET.get('result') # param2の値を取得
    context = {
            'file_url' : file_url,
            'message': 'result',
            'Laundry': ['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 'L9', 'LA', 'LB', 'LC', 'L1', 'LD', 'LE'],
            'Bleach' : ['B1', 'B2', 'B3'],
            'Nature' : ['N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'N8'],
            'Iron' : ['I1', 'I2', 'I3', 'I4'],
            'Tumble' : ['T1', 'T2', 'T3'],
            'Dry' : ['D1', 'D2', 'D3', 'D4', 'D5'],
            'Wet' : ['W1', 'W2', 'W3', 'W4' ],
            'results': json.dumps(results),
        }
    return render(request, 'laundry_tag_check/index.html', context)
    
def judge_result(request):
    #継承するfile_url = judge.file_url
    #画像消す

    return render(request, 'home/index.html')