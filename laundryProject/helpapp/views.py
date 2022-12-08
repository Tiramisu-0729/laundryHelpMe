from django.urls import reverse
from urllib.parse import urlencode
from django.shortcuts import render

from .models import Cabinet, Categories, Profile
from django.shortcuts import redirect, render, get_object_or_404
from .forms import CabinetForm, JudgeForm, ProfileForm, UpdateUserForm, UpdateProfileForm
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import csv
import torch
import json


def helpapp(request):
    #ログインがあるか判別
    if request.user.is_authenticated :
        return home(request)
    else :
        return render(request, 'helpapp/index.html')

def register(request):
    return render(request, 'helpapp/register.html')

def nologin(request):
    context = {
        'ON' : json.dumps('home'),
        'message': 'Judge',
        'form': JudgeForm(),
    }
    return render(request, 'home/index.html', context)

def home(request):
    context = {
        'ON' : json.dumps('home'),
        'message': 'Judge',
        'form': JudgeForm(),
    }
    return render(request, 'home/index.html', context)
    
    
def washer(request):
    if request.user.is_authenticated :
        washers =[]
        tags=[]
        i=0
        if 'washers' in request.session:
            IDs = request.session.get('washers')
            for id in IDs:
                if Cabinet.objects.filter(pk=id).exists():
                    washers.append(Cabinet.objects.get(pk=id))
            for washer in washers:
                tags = washer.laundry_tag.split(',')
                washers[i].laundry_tag = tags[0]
                i+=1
        categories=["tops", "bottoms","outer","inner","other"]
        context = {
            'categories' : categories,
            'ON' : json.dumps('washer'),
            'message': 'Washer',
            'washers' : washers
        }
        return render(request, 'washer/index.html',context)
    else :
        return redirect('/accounts/login/')

def washer_add(request):
    if request.user.is_authenticated :
        user = request.user
        cabs = Cabinet.objects.filter(author=user)
        cabinets =[]
        for cabinet in cabs :
            tags = cabinet.laundry_tag.split(',')
            if not(tags[0] == 'LD' or tags[0] == 'LE'):
                cabinets.append(cabinet)
        context = {
            'ON' : json.dumps('washer'),
            'message': 'Washer',
            'cabinets' : cabinets,
            'user' : user,
        }
        return render(request, 'washer/add.html',context)
    else :
        return redirect('/accounts/login/')

def washer_add_redirect(request):
    if request.user.is_authenticated :
        # del request.session['washers']
        if request.method == "POST":
            checks_value = request.POST.getlist('check')
            washers = request.session.get('washers')
            if washers != None:
                for value in checks_value:
                    washers.append(value)
            else:
                washers = checks_value
            request.session['washers'] = (washers) 
        return redirect('/helpapp/washer')
    else :
        return redirect('/accounts/login/')

def washer_judge(request):
    if request.user.is_authenticated :
        if 'washers' in request.session:
            washers=[]
            IDs = request.session.get('washers')
            for id in IDs:#washersを取り出す
                if Cabinet.objects.filter(pk=id).exists():
                    washers.append(Cabinet.objects.get(pk=id))
            comp = ["L1", "B1", "T1"]
            for washer in washers:
                tags = washer.laundry_tag.split(',')
                for tag in tags:
                    if tag[0] == "L":
                        if int(tag[1], 16) > int(comp[0][1] ,16):#一番条件が厳しいタグの判定
                            comp[0]=tag
                    elif tag[0] == "B":
                        if int(tag[1], 16) > int(comp[1][1] ,16):#一番条件が厳しいタグの判定
                            comp[1]=tag
                    elif tag[0] == "T":
                        if int(tag[1], 16) > int(comp[2][1] ,16):#一番条件が厳しいタグの判定
                            comp[2]=tag
            context = {
                'washers' : washers,
                'comp' : comp,
                'ON' : json.dumps('washer'),
                'message': 'Washer',
            }
            return render(request, 'washer/result.html', context)
        return redirect('/helpapp/washer/')
    else :
        return redirect('/accounts/login/')

def washers_delete(request):
    if request.user.is_authenticated :
        # del request.session['washers']
        if request.method == "POST":
            checks_value = request.POST.getlist('check')
            washers = request.session.get('washers')
            for value in checks_value:
                if value in washers:
                    washers.remove(value)
            request.session['washers'] = washers
        return redirect('/helpapp/washer')
    else :
        return redirect('/accounts/login/')


def washer_clear(request):
    if request.user.is_authenticated :
        del request.session['washers']
        return redirect('/helpapp/washer')
    else :
        return redirect('/accounts/login/')

def cabinet(request):
    if request.user.is_authenticated :
        user = request.user
        cabinets = Cabinet.objects.filter(author=user)
        i=0
        for cabinet in cabinets:
            tags = cabinet.laundry_tag.split(',')
            cabinets[i].laundry_tag = tags[0]
            i+=1
        none = ""
        if not(cabinets.exists):
            none = "タンスに登録してください"
        categories=["tops", "bottoms","outer","inner","other"]
        context = {
            'ON' : json.dumps('cabinet'),
            'message': 'Cabinet',
            'cabinets' : cabinets,
            'user' : user,
            'none':none,
            'categories':categories
        }
        return render(request, 'cabinet/index.html', context)
    else :
        return redirect('/accounts/login/')

def cabinet_judge(request):
    if request.user.is_authenticated :
        user = request.user
        context = {
            'ON' : json.dumps('cabinet'),
            'message': 'Cabinet',
            'cabinet_message' : '洗濯タグを撮影してください',
            'user': user,
            'form': JudgeForm(),
        }
        return render(request, 'home/index.html', context)
    else :
        return redirect('/accounts/login/')

def cabinet_form(request):
    if request.user.is_authenticated :
        context = {
            'ON' : json.dumps('cabinet'),
            'message': 'Add Cabinet',
            'user': user,
            'cabinet_form': CabinetForm(),
        }
        return render(request, 'cabinet/add.html', context)
    else :
        return redirect('/accounts/login/')

def cabinet_add(request):
    if request.method == "POST":
        form = CabinetForm(request.POST)
        if form.is_valid():#formの内容が正しければ
            cabinet = Cabinet()
            cabinet.author = request.user
            cabinet.name = request.POST['name']
            cabinet.memo = request.POST['memo']
            cabinet.category = Categories(request.POST['category'])#category型じゃないと怒られた
            cabinet.laundry_tag = request.session.get('tags')#判定結果sessionとか
            cabinet.image = request.FILES['image']#保存先はupload_img＞upload_img>imgのなか
            cabinet.save()
            
        return redirect('/helpapp/cabinet')
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
    tags = cabinet.laundry_tag.split(',')
    context = {
        'ON' : json.dumps('cabinet'),
        'tags' : tags,
        'message': cabinet.name,
        'cabinet' : cabinet,
    }
    return render(request, 'cabinet/detail.html', context)

def cabinet_delete(request, pk):
    cabinet = Cabinet.objects.get(pk=pk)
    cabinet.delete()
    return redirect('/helpapp/cabinet')

def cabinets_delete(request):
    if request.user.is_authenticated :
        # del request.session['washers']
        if request.method == "POST":
            checks_value = request.POST.getlist('check')
            for value in checks_value:
                cabinet = Cabinet.objects.get(pk=value)
                cabinet.delete()
        return redirect('/helpapp/cabinet')
    else :
        return redirect('/accounts/login/')


def user(request):
    if request.user.is_authenticated :
        if request.method == 'POST':
            profile = Profile.objects.filter(user=request.user).first()
            user_form = UpdateUserForm(request.POST, instance=request.user)
            profile_form = UpdateProfileForm(request.POST, request.FILES, instance=profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                new_profile=Profile()
                new_profile=profile_form.save(commit=False)
                new_profile.user = request.user
                new_profile.save()
                messages.success(request, 'Your profile is updated successfully')
                return redirect('/helpapp/user')
        else:
            profile = Profile.objects.filter(user=request.user).first()
            user_form = UpdateUserForm(instance=request.user)
            profile_form = UpdateProfileForm(instance=profile)
        #本番は消して from laundryProject.settings import *　をする ↓
        STATIC_ROOT = 'C:/Users/20jz0144/Documents/GitHub/laundryHelpMe/laundryProject/helpapp/static'
        # STATIC_ROOT = 'G:/マイドライブ/Python/laundryHelpMe/laundryProject/helpapp/static'
        # STATIC_ROOT = 'C:/Users/20jz0107/Documents/GitHub/laundryHelpMe/laundryProject/helpapp/static'
        user = request.user
        tables = [
            ['washingProcesses','洗濯処理'], 
            ['bleachingProcesses','漂白処理'], 
            ['tumbleDrys','タンブル乾燥'], 
            ['naturalDrys','自然乾燥'], 
            ['ironFinishs','アイロン仕上げ'], 
            ['dryCleanings','ドライクリーニング'], 
            ['wetCleanings','ウエットクリーニング'], 
            ['info', '注意事項']
            ]
        washingProcesses, bleachingProcesses, tumbleDrys, naturalDrys, ironFinishs, dryCleanings, wetCleanings, info = [],[],[],[],[],[],[],[]
        # CSV読み込み
        with open(STATIC_ROOT + '/csv/washingProcesses.csv',encoding="utf-8") as f:
            for row in csv.reader(f):
                washingProcesses.append(row)
        with open(STATIC_ROOT + '/csv/bleachingProcesses.csv',encoding="utf-8") as f:
            for row in csv.reader(f):
                bleachingProcesses.append(row)
        with open(STATIC_ROOT + '/csv/tumbleDrys.csv',encoding="utf-8") as f:
            for row in csv.reader(f):
                tumbleDrys.append(row)
        with open(STATIC_ROOT + '/csv/naturalDrys.csv',encoding="utf-8") as f:
            for row in csv.reader(f):
                naturalDrys.append(row)
        with open(STATIC_ROOT + '/csv/ironFinishs.csv',encoding="utf-8") as f:
            for row in csv.reader(f):
                ironFinishs.append(row)
        with open(STATIC_ROOT + '/csv/dryCleanings.csv',encoding="utf-8") as f:
            for row in csv.reader(f):
                dryCleanings.append(row)
        with open(STATIC_ROOT + '/csv/wetCleanings.csv',encoding="utf-8") as f:
            for row in csv.reader(f):
                wetCleanings.append(row)
        f = open(STATIC_ROOT + '/csv/info.txt', 'r', encoding='UTF-8')
        info = f.read()
        f.close
        profile = Profile.objects.filter(user=user).first()
        sumCabinet = Cabinet.objects.filter(author=user).count()
        context = {
            'ON' : json.dumps('user'),
            'message': 'User',
            'profile' : profile,
            'sumCabinet': sumCabinet,
            'user': user,
            'washingProcesses': washingProcesses,
            'bleachingProcesses': bleachingProcesses,
            'tumbleDrys': tumbleDrys,
            'naturalDrys': naturalDrys,
            'ironFinishs': ironFinishs,
            'dryCleanings': dryCleanings,
            'wetCleanings': wetCleanings,
            'info': info,
            'tables': tables,
            'user_form': user_form, 
            'profile_form': profile_form,
        }
        return render(request, 'user/index.html', context)
    else :
        return redirect('/accounts/login/')

def timeline(request):
    if request.user.is_authenticated :
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
        none=""
        if not(cabinets.exists):
            none = "タンスに登録してください"
        context = {
            'ON' : json.dumps('timeline'),
            'tag_list': tag_list,
            'message': 'TimeLine',
            'cabinets' : TimeLineCab,
            'none' : none
        }
        return render(request, 'timeline/index.html', context)
    else :
        return redirect('/accounts/login/')

def judge(request):
    if request.method == "POST":
        image = request.FILES['UploadImg']#保存先はupload_imgのなか　いったん保存
        fs = FileSystemStorage()
        file_data = fs.save(image.name, image)
        file_url = fs.url(file_data)
        request.session['file_url'] = file_url
        #AIで画像判定
        path_hubconfig = "yolo"
        path_weightfile = "yolo/729x300_yolov5m_best.pt" 
        model = torch.hub.load(path_hubconfig, 'custom',path=path_weightfile, source='local')
        results = model(file_url.lstrip("/"))

        #判定結果 解析
        datas = json.loads(results.pandas().xyxy[0].to_json(orient="values"))
        result=[]
        for data in datas :
            if data[4] > 0.5:
                result.append(data[6]) 
        redirect_url = reverse('helpapp:laundry_tag_check')
        parameters = urlencode({'file_url': file_url, 'result' : result})
        url = f'{redirect_url}?{parameters}'
        return redirect(url)
    else:
        user = request.user
        context = {
            'ON' : json.dumps('home'),
            'message': 'judge',
            'user': user,
            'form': JudgeForm(),
        }
    return render(request, 'home/index.html', context)

def laundry_tag_check(request):
    file_url = request.GET.get('file_url') # param1の値を取得
    results = request.GET.get('result') # param2の値を取得
    context = {
        'ON' : json.dumps('home'),
        'file_url' : file_url,
        'message': 'Select',
        'Laundry': ['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 'L9', 'LA', 'LB', 'LC', 'LD', 'LE'],
        'Bleach' : ['B1', 'B2', 'B3'],
        'Nature' : ['N1', 'N2', 'N3', 'N4', 'N6', 'N5', 'N7', 'N8'],
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
        file_url = request.session.get('file_url')
        context = {
            'ON' : json.dumps('home'),
            'message': 'Result',
            'result' : result,
            'file_url' : file_url,
            'tags' : tags,
        }
    
    #ディレクトリ削除os.remove('target.txt')
    return render(request, 'laundry_tag_check/result.html', context)

import torch
from django.shortcuts import render

def testYolo(request):
    path_hubconfig = "yolo"
    path_weightfile = "yolo/729x300_yolov5m_best.pt" 
    img_path = '/upload_img/4018.jpg'
    model = torch.hub.load(path_hubconfig, 'custom',path=path_weightfile, source='local')
    results = model(img_path.lstrip("/"))
    datas = json.loads(results.pandas().xyxy[0].to_json(orient="values"))
    tags=[]
    for data in datas :
        if data[4] > 0.5:
            tags.append(data[6]) 
    context = {
        'message': 'Test',
        'model': model,
        'results': results,
        'xyxy': results.pandas().xyxy[0].to_json(orient="values"),
        'tags': tags,
        'datas': datas,
    }
    return render(request, 'testYolo/test.html', context)