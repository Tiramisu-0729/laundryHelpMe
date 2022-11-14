from distutils.command.upload import upload
import json
import os
from django.test import tag
from django.urls import reverse
from urllib.parse import urlencode
import torch
from django.shortcuts import render

from .models import Cabinet, Categories
from django.shortcuts import redirect, render, get_object_or_404
from .forms import CabinetForm, JudgeForm
from django.core.files.storage import FileSystemStorage
from django.views.generic import TemplateView

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
    
def washer(request):
    context = {
        'message': 'Laundry',
    }
    return render(request, 'washer/index.html',context)

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
            cabinet.laundry_tag = request.session['tags']#判定結果sessionとか
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
        if 19 < cnt:
            break
        cab.laundry_tag = cab.laundry_tag.split(',') #cabinetのlaundry_tagを「，」で区切って配列化
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
        request.session['file_url'] = file_url
        #AIで画像判定
        path_hubconfig = "laundryHelpMe/laundryProject/yolo"
        path_weightfile = "laundryHelpMe/laundryProject/yolo/729x300_yolov5m_best.pt" 
        model = torch.hub.load(path_hubconfig, 'custom',path=path_weightfile, source='local')
        results = model(file_url.lstrip("/"))

        #判定結果 解析
        datas = json.loads(results.pandas().xyxy[0].to_json(orient="values"))
        result=[]
        for data in datas :
            if data[4] > 0.5:
                result.append(data[6]) 
        
        # result = "L8,B3,T3,N1,I4"#ここに結果を入れる
        # result = result.split(',') 
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
            'message': 'select',
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
    if request.method == "POST":
        tags = []
        names=['Laundry','Bleach','Nature','Iron','Tumble','Dry','Wet']
        for name in names:
            if request.POST.get(name) == None:
                print("none")
            else:
                tags.append(request.POST.get(name))
        if tags[0] == "LE":
            result = "洗えません"
        elif tags[0] == "LD":
            result = "手洗い"
        else:
            result ="洗えます"
        dbtag = ",".join(tags)
        request.session['tags'] = dbtag
        file_url = request.session['file_url']
        context = {
            'message': 'result',
            'result' : result,
            'file_url' : file_url,
            'tags' : tags,
        }
    
    #ディレクトリ削除os.remove('target.txt')

    return render(request, 'laundry_tag_check/result.html', context)

import torch
from django.shortcuts import render

def testYolo(request):
    path_hubconfig = "laundryHelpMe/laundryProject/yolo"
    path_weightfile = "laundryHelpMe/laundryProject/yolo/729x300_yolov5m_best.pt" 
    img_path = '/upload_img/4018.jpg'
    model = torch.hub.load(path_hubconfig, 'custom',path=path_weightfile, source='local')
    results = model(img_path.lstrip("/"))
    datas = json.loads(results.pandas().xyxy[0].to_json(orient="values"))
    tags=[]
    for data in datas :
        if data[4] > 0.5:
            tags.append(data[6]) 
    context = {
        'message': 'test',
        'model': model,
        'results': results,
        'xyxy': results.pandas().xyxy[0].to_json(orient="values"),
        'tags': tags,
    }
    return render(request, 'testYolo/test.html', context)
    
class IndexView(TemplateView):
    template_name = 'user/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        words = ['1', '2', '3', '4', '5', '6']
        context["washingDisplay"] = words
        return context
