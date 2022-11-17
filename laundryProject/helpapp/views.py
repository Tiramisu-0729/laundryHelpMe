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
    if request.user.is_authenticated :
        user = request.user
        context = {
            'message': 'Judage',
            'user': user,
            'form': JudgeForm(),
        }
        return render(request, 'home/index.html', context)
    else :
        return render(request, 'helpapp/index.html')
    
    
def washer(request):
    if request.user.is_authenticated :
        washers = request.session.get('washers')
        context = {
            'message': 'Washer',
            'washers' : washers
        }
        return render(request, 'washer/index.html',context)
    else :
        return render(request, 'helpapp/index.html')

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
            'message': 'Washer',
            'cabinets' : cabinets,
            'user' : user,
        }
        return render(request, 'washer/add.html',context)
    else :
        return render(request, 'helpapp/index.html')

def washer_judge(request):
    if request.user.is_authenticated :
        washers = request.session.get('washers')
        context = {
            'message': 'Washer',
            'washers': washers,
            'form': JudgeForm(),
        }
        return render(request, 'home/index.html', context)
    else :
        return render(request, 'helpapp/index.html')


def cabinet(request):
    if request.user.is_authenticated :
        user = request.user
        cabinets = Cabinet.objects.filter(author=user)
        none = ""
        if not(cabinets.exists):
            none = "タンスに登録してください"
        context = {
            'message': 'Cabinet',
            'cabinets' : cabinets,
            'user' : user,
            'none':none
        }
        return render(request, 'cabinet/index.html', context)
    else :
        return render(request, 'helpapp/index.html')

def cabinet_judge(request):
    if request.user.is_authenticated :
        user = request.user
        context = {
            'message': 'Cabinet',
            'cabinet_message' : '洗濯タグを撮影してください',
            'user': user,
            'form': JudgeForm(),
        }
        return render(request, 'home/index.html', context)
    else :
        return render(request, 'helpapp/index.html')

def cabinet_form(request):
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
        'tags' : tags,
        'message': cabinet.name,
        'cabinet' : cabinet,
    }
    return render(request, 'cabinet/detail.html', context)
    
def user(request):
    user = request.user
    context = {
        'message': 'User',
        'user': user,
        'washingProcesses': [
            '<img src="/static/pictures/L1.png"', '液温は95°Cを限度とし、<br>洗濯機で通常の洗濯処理ができる。', '<img src="/static/pictures/101.png"',
            '<img src="/static/pictures/L2.png"', '液温は70°Cを限度とし、<br>洗濯機で通常の洗濯処理ができる。', '<img src="/static/pictures/white.png"',
            '<img src="/static/pictures/L3.png"', '液温は60°Cを限度とし、<br>洗濯機で通常の洗濯処理ができる。', '<img src="/static/pictures/102.png"',
            '<img src="/static/pictures/L4.png"', '液温は60°Cを限度とし、<br>洗濯機で弱い洗濯処理ができる。', '<img src="/static/pictures/white.png"',
            '<img src="/static/pictures/L5.png"', '液温は50°Cを限度とし、<br>洗濯機で通常の洗濯処理ができる。', '<img src="/static/pictures/white.png"',
            '<img src="/static/pictures/L6.png"', '液温は50°Cを限度とし、<br>洗濯機で弱い洗濯処理ができる。', '<img src="/static/pictures/white.png"',
            '<img src="/static/pictures/L7.png"', '液温は40°Cを限度とし、<br>洗濯機で通常の洗濯処理ができる。', '<img src="/static/pictures/103.png"', 
            '<img src="/static/pictures/L8.png"', '液温は40°Cを限度とし、<br>洗濯機で弱い洗濯処理ができる。', '<img src="/static/pictures/104.png"', 
            '<img src="/static/pictures/L9.png"', '液温は40°Cを限度とし、<br>洗濯機で非常に弱い洗濯処理ができる。', '<img src="/static/pictures/white.png"',
            '<img src="/static/pictures/LA.png"', '液温は30°Cを限度とし、<br>洗濯機で通常の洗濯処理ができる。', '<img src="/static/pictures/white.png"',
            '<img src="/static/pictures/LB.png"', '液温は30°Cを限度とし、<br>洗濯機で弱い洗濯処理ができる。', '<img src="/static/pictures/105.png"', 
            '<img src="/static/pictures/LC.png"', '液温は30°Cを限度とし、<br>洗濯機で非常に弱い洗濯処理ができる。', '<img src="/static/pictures/white.png"',
            '<img src="/static/pictures/LD.png"', '液温は40°Cを限度とし、<br>手洗いによる洗濯処理ができる。', '<img src="/static/pictures/106.png"', 
            '<img src="/static/pictures/LE.png"', '洗濯処理はできない。', '<img src="/static/pictures/107.png"'
        ],
        'bleachingProcesses': [
            '<img src="/static/pictures/B1.png"', '塩素系及び酸素系漂白剤による漂白処理ができる。', '<img src="/static/pictures/201.png"',
            '<img src="/static/pictures/B2.png"', '酸素系漂白剤による漂白処理ができるが、<br>塩素系漂白剤による漂白処理はできない。', '<img src="/static/pictures/white.png"',
            '<img src="/static/pictures/B3.png"', '漂白処理はできない。', '<img src="/static/pictures/202.png"'
        ],
        'tumbleDrys': [
            '<img src="/static/pictures/T1.png"', '洗濯処理後のタンブル乾燥処理ができる。<br>高温乾燥：排気温度の上限は最高80°C', '<img src="/static/pictures/white.png"',
            '<img src="/static/pictures/T2.png"', '洗濯処理後のタンブル乾燥処理ができる。<br>低温乾燥：排気温度の上限は最高60°C', '<img src="/static/pictures/white.png"',
            '<img src="/static/pictures/T3.png"', '洗濯処理後のタンブル乾燥処理はできない。', '<img src="/static/pictures/white.png"'
        ],
        'naturalDrys': [
            '<img src="/static/pictures/N1.png"', 'つり干し乾燥がよい。', '<img src="/static/pictures/601.png"',
            '<img src="/static/pictures/N6.png"', '日陰でのつり干し乾燥がよい。', '<img src="/static/pictures/602.png"',
            '<img src="/static/pictures/N2.png"', 'ぬれつり干し乾燥がよい。', '<img src="/static/pictures/white.png"',
            '<img src="/static/pictures/N5.png"', '日陰でのぬれつり干し乾燥がよい。', '<img src="/static/pictures/white.png"',
            '<img src="/static/pictures/N3.png"', '平干し乾燥がよい。', '<img src="/static/pictures/603.png"',
            '<img src="/static/pictures/N7.png"', '日陰での平干し乾燥がよい。', '<img src="/static/pictures/604.png"',
            '<img src="/static/pictures/N4.png"', 'ぬれ平干し乾燥がよい。', '<img src="/static/pictures/white.png"',
            '<img src="/static/pictures/N8.png"', '日陰でのぬれ平干し乾燥がよい。', '<img src="/static/pictures/white.png"'
        ],
        'ironFinishs': [
            '<img src="/static/pictures/I1.png"', '底面温度200°Cを限度として<br>アイロン仕上げ処理ができる。', '<img src="/static/pictures/301.png"',
            '<img src="/static/pictures/I2.png"', '底面温度150°Cを限度として<br>アイロン仕上げ処理ができる。', '<img src="/static/pictures/302.png"',
            '<img src="/static/pictures/I3.png"', '底面温度110°Cを限度として<br>アイロン仕上げ処理ができる。', '<img src="/static/pictures/303.png"',
            '<img src="/static/pictures/I4.png"', 'アイロン仕上げ処理はできない。', '<img src="/static/pictures/304.png"'
        ],
        'dryCleanings': [
            '<img src="/static/pictures/D1.png"', 'パークロロエチレン及び記号Fの欄に規定の溶剤での通常のドライクリーニング処理ができる。', '<img src="/static/pictures/401.png"',
            '<img src="/static/pictures/D2.png"', 'パークロロエチレン及び記号Fの欄に規定の溶剤での弱いドライクリーニング処理ができる。', '<img src="/static/pictures/white.png"',
            '<img src="/static/pictures/D3.png"', '石油系溶剤(蒸留温度150°C～210°C、引火点38°C～)での通常のドライクリーニング処理ができる。', '<img src="/static/pictures/402.png"',
            '<img src="/static/pictures/D4.png"', '石油系溶剤(蒸留温度150°C～210°C、引火点38°C～)での弱いドライクリーニング処理ができる。', '<img src="/static/pictures/white.png"',
            '<img src="/static/pictures/D5.png"', 'ドライクリーニング処理ができない。', '<img src="/static/pictures/403.png"'
        ],
        'wetCleanings': [
            '<img src="/static/pictures/W1.png"', '通常のウエットクリーニング処理ができる。', '<img src="/static/pictures/white.png"',
            '<img src="/static/pictures/W2.png"', '弱いウエットクリーニング処理ができる。', '<img src="/static/pictures/white.png"',
            '<img src="/static/pictures/W3.png"', '非常に弱いウエットクリーニング処理ができる。', '<img src="/static/pictures/white.png"',
            '<img src="/static/pictures/W4.png"', 'ウエットクリーニング処理はできない。', '<img src="/static/pictures/white.png"'
        ],
        'list': 
            '<ol>'
                '<li>洋服に洗濯タグ(洗濯表示)がなければ<br>このサイトは使用できません</li><br>'
                '<li>たんす機能はログインしていなければ<br>使用できません</li><br>'
                '<li>洗濯タグは正しい向きで撮影してください</li><br>'
                '<li>以下の素材が含まれている洋服は<br>自宅では洗濯できません<br><br>'
                '<font color="red">絹、レーヨン、キュプラ、<br>アセテート、皮革、毛皮用品</font></li><br>'
                '<li>以下の洋服はクリーニング店に<br>相談してください<br><br>'
                '<font color="red">スーツ(ウォッシャブルを除く)、<br>ジャケット、コート、ネクタイ、和服</font></li><br>'
                '<li>自宅で洗濯する際には、色落ちなどを確認し<br>(色落ちする洋服は洗濯できません)、<br>自己責任でおこなってください</li><br>'
                '<li>洗濯表示に注意事項が記載されている場合は、<br>それに従ってください</li><br>'
            '</ol>'
    }
    return render(request, 'user/index.html', context)

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
            'tag_list': tag_list,
            'message': 'TimeLine',
            'cabinets' : TimeLineCab,
            'none' : none
        }
        return render(request, 'timeline/index.html', context)
    else :
        return render(request, 'helpapp/index.html')

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
        file_url = request.session.get('file_url')
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
        'message': 'test',
        'model': model,
        'results': results,
        'xyxy': results.pandas().xyxy[0].to_json(orient="values"),
        'tags': tags,
        'datas': datas,
    }
    return render(request, 'testYolo/test.html', context)