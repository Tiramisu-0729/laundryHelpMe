import os
import shutil
from django.urls import reverse
from urllib.parse import urlencode
from django.shortcuts import render
from laundryProject.settings import MEDIA_ROOT
from .models import Cabinet, Categories, Profile, Washer_log, Laundry, Report
from django.shortcuts import redirect, render, get_object_or_404
from .forms import CabinetForm, JudgeForm, UpdateUserForm, UpdateProfileForm, MyPasswordChangeForm
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import json
from django.contrib import messages
from helpapp.data_load import MODEL,tables

def helpapp(request):
    #ログインがあるか判別
    if request.user.is_authenticated :
        return home(request)
    else :
        return redirect('/accounts/login/')

def register(request):
    return render(request, 'helpapp/register.html')

def nologin(request):
    context = {
        'ON' : json.dumps('home'),
        'message': 'Judge',
        'form': JudgeForm(),
        'tables': tables,
    }
    return render(request, 'nologin/index.html', context)

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
        none=1
        if 'washers' in request.session:
            IDs = request.session.get('washers')
            for id in IDs:
                if Cabinet.objects.filter(pk=id).exists():#存在確認
                    washers.append(Cabinet.objects.get(pk=id))
            for washer in washers:
                tags = washer.laundry_tag.split(',')
                washers[i].laundry_tag = tags[0]
                i+=1
        categories = Categories.objects.all()
        categories_json =[]
        
        for category in categories:
            categories_json.append(category.name)
        if len(washers) == 0:
            none = 0
        context = {
            'categories_json' : json.dumps(categories_json), 
            'categories' : categories,
            'ON' : json.dumps('washer'),
            'message': 'Washer',
            'none' : none,
            'none_json' : json.dumps(none),
            'washers' : washers
        }
        return render(request, 'washer/index.html',context)
    else :
        return redirect('/accounts/login/')

def washer_add(request):
    if request.user.is_authenticated :
        user = request.user
        cabs = Cabinet.objects.filter(author=user)  
        cabs = list(cabs.values())
        if 'washers' in request.session:
            IDs = request.session.get('washers')  
            for ID in IDs :
                i=0
                for cab in cabs :
                    if int(ID) == int(cab["id"]) :
                        del cabs[i]
                        break
                    i += 1
        cabinets =[]
        for cabinet in cabs :
            tags = cabinet["laundry_tag"].split(',')
            if not(tags[0] == 'LD' or tags[0] == 'LE'):
                cabinets.append(Cabinet.objects.get(pk=cabinet["id"]))
        error=""
        if(len(cabinets) == 0):
            error = "追加できる洗濯物がありません"
        context = {
            'ON' : json.dumps('washer'),
            'message': 'Washer',
            'cabinets' : cabinets,
            'user' : user,
            'error' : error
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
        messages.success(request, '登録内容を保存しました。')
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
                'comp_json' : json.dumps(comp),
                'ON' : json.dumps('washer'),
                'message': 'Washer',
            }
            return render(request, 'washer/result.html', context)
        return redirect('/helpapp/washer')
    else :
        return redirect('/accounts/login/')

def washer_complete(request) :
    profile = Profile.objects.filter(user=request.user).first()
    profile.washer_cnt += 1
    profile.save()
    return redirect('/helpapp/washer')

def washers_delete(request):
    if request.user.is_authenticated :
        if request.method == "POST":
            checks_value = request.POST.getlist('check')
            washers = request.session.get('washers')
            for value in checks_value:
                if value in washers:
                    washers.remove(value)
            request.session['washers'] = washers
        messages.success(request, '削除しました')
        return redirect('/helpapp/washer')
    else :
        return redirect('/accounts/login/')

def washer_log(request):
    if request.user.is_authenticated :
        user = request.user
        laundries=[]
        washer_logs = []
        if Washer_log.objects.filter(user=user).exists():   #存在確認
            washer_logs = Washer_log.objects.filter(user=user).order_by("-created_at")
            for washer_log in washer_logs:
                if  Laundry.objects.filter(washer_log_id = washer_log.pk).exists():   #存在確認
                    laundries.append(Laundry.objects.filter(washer_log_id = washer_log.pk)) #laundry表とcabinet表を結合
        context = {
            'ON' : json.dumps('timeline'),
            'message': 'timeline',
            'washer_logs' : washer_logs,
            'Laundries' : laundries,
            'user' : user,
        }
        return render(request, 'washer_log/index.html', context)
    else :
        return redirect('/accounts/login/')

def washer_log_add(request):
    if request.user.is_authenticated :
        if 'washers' in request.session:
            Laundries=[]
            IDs = request.session.get('washers')
            for id in IDs:#washersを取り出す
                if Cabinet.objects.filter(pk=id).exists():
                    Laundries.append(Cabinet.objects.get(pk=id))
            washer_log = Washer_log()
            washer_log.user = request.user
            washer_log.save()
            for Laund in Laundries:
                laundry = Laundry()
                laundry.washer_log_id = Washer_log(washer_log.pk)
                laundry.cabinet_id = Cabinet(Laund.pk)
                laundry.save()
            messages.success(request, '洗濯物を保存しました')
            return redirect('/helpapp/washer')
        return redirect('/helpapp/washer/')
    else :
        return redirect('/accounts/login/')

def washer_log_detail(request, pk):
    if request.user.is_authenticated :
        if  Laundry.objects.filter(washer_log_id = pk).exists():   #存在確認
            laundry = Laundry.objects.filter(washer_log_id = pk) #laundry表とcabinet表を結合
            comp = ["L1", "B1", "T1"]
            for laund in laundry:
                tags = laund.cabinet.laundry_tag.split(',')
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
                'laundry' : laundry,
                'comp' : comp,
                'comp_json' : json.dumps(comp),
                'ON' : json.dumps('timeline'),
                'message': 'Washer',
            }
            return render(request, 'washer_log/detail.html', context) 
        return redirect('/helpapp/washer/')
    else :
        return redirect('/accounts/login/')

def washer_log_delete(request, pk):
    if request.user.is_authenticated :
        if  Washer_log.objects.filter(washer_log_id = pk).exists():   #存在確認
            washer_log = Washer_log.objects.filter(washer_log_id = pk) #Washer_log
            washer_log.delete()
            messages.success(request, '削除しました')
            return redirect('/helpapp/washer_log')
        return redirect('/helpapp/washer_log')
    else :
        return redirect('/accounts/login/')


def washer_clear(request):
    if request.user.is_authenticated :
        del request.session['washers']
        profile = Profile.objects.filter(user=request.user).first()
        profile.washer_cnt += 1
        profile.save()
        messages.success(request, '洗濯物を空にしました')
        return redirect('/helpapp/washer')
    else :
        return redirect('/accounts/login/')

def cabinet(request):
    if request.user.is_authenticated :
        user = request.user
        cabinets = Cabinet.objects.filter(author=user)
        categories = Categories.objects.all()
        i=0
        categories_json =[]
        for category in categories:
            categories_json.append(category.name)
        for cabinet in cabinets:
            tags = cabinet.laundry_tag.split(',')
            cabinets[i].laundry_tag = tags[0]
            i+=1
        none = ""
        if not(cabinets.exists):
            none = "タンスに登録してください"
        context = {
            'categories' : categories,
            'categories_json' : json.dumps(categories_json), #serializers.serialize("json", categories),
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
            messages.success(request, '登録しました')
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
    if Cabinet.objects.filter(pk=pk).exists():#存在確認
        cabinet = Cabinet.objects.get(pk=pk)
        cabinet.delete()
    messages.success(request, '削除しました')
    return redirect('/helpapp/cabinet')

def cabinets_delete(request):
    if request.user.is_authenticated :
        # del request.session['washers']
        if request.method == "POST":
            checks_value = request.POST.getlist('check')
            for value in checks_value:
                if Cabinet.objects.filter(pk=value).exists():#存在確認
                    cabinet = Cabinet.objects.get(pk=value)
                    cabinet.delete()
        messages.success(request, '削除しました')
        return redirect('/helpapp/cabinet')
    else :
        return redirect('/accounts/login/')

def user(request):
    if request.user.is_authenticated :
        if Profile.objects.filter(user=request.user).exists():
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
                    messages.success(request, 'プロフィールが変更されました。')
                    return redirect('/helpapp/user')
            else:
                profile = Profile.objects.filter(user=request.user).first()
                user_form = UpdateUserForm(instance=request.user)
                profile_form = UpdateProfileForm(instance=profile)
                user = request.user
                profile = Profile.objects.filter(user=user).first()
                sumCabinet = Cabinet.objects.filter(author=user).count()
                awards = [["服の総数", sumCabinet], ["判定回数", profile.judge_cnt], ["洗濯回数", profile.washer_cnt]]
                for award in awards:
                    if award[1] >= 200 :
                        award.append('gold+α')
                    elif award[1] >= 100 :
                        award.append('gold')
                    elif award[1] >= 50 :
                        award.append('silver')
                    elif award[1] >= 20:
                        award.append('bronze')
                    else :
                        award.append('none')
                context = {
                    'ON' : json.dumps('user'),
                    'message': 'User',
                    'profile' : profile,
                    'awards': awards,
                    'user': user,
                    'tables': tables, # model_loadからtables読み込み
                    'user_form': user_form, 
                    'profile_form': profile_form,
                }
                return render(request, 'user/index.html', context)
        else:
            new_profile=Profile()
            new_profile.user = request.user
            new_profile.image = "none"
            new_profile.save()
        return redirect('/helpapp/user')
    else :
        return redirect('/accounts/login/')

def changePass(request):
    if request.user.is_authenticated :
        if request.method == 'POST':
            form = MyPasswordChangeForm(request.POST)
            if form.is_valid():
                form.save()
            return redirect('/helpapp/user')
        else :
            pass_form = MyPasswordChangeForm(user=request.user)
            context = {
                'pass_form': pass_form,
                'ON' : json.dumps('user'),
                'message': 'ChangePass',
            }
            return render(request, 'user/change.html', context)

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
        ext = os.path.splitext(image.name)
        file_data = fs.save(request.user.username + ext[1], image)
        file_url = fs.url(file_data)
        request.session['file_url'] = file_url
        #AIで画像判定
        import time
        time.sleep(0.1)
        # results = MODEL(file_url)
        results = MODEL(file_url.lstrip("/")) # model_loadからMODEL読み込み
        #判定結果 解析
        datas = json.loads(results.pandas().xyxy[0].to_json(orient="values"))
        result=[]
        for data in datas :
            if data[4] > 0.5:
                result.append(data[6]) 
        redirect_url = reverse('helpapp:laundry_tag_check')
        parameters = urlencode({'file_url': file_url, 'result' : result})
        url = f'{redirect_url}?{parameters}'
        if request.user.is_authenticated :
            profile = Profile.objects.filter(user=request.user).first()
            profile.judge_cnt += 1
            profile.save()
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
    res = request.GET.get('result') # param2の値を取得
    res = res.replace("[","").replace("]","").replace("'","").replace(" ","")
    request.session['ai_result'] = res
    results = res.split(',')
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
    context=[]
    if request.method == "POST":
        tags = []
        names=['Laundry','Bleach','Nature','Iron','Tumble','Dry','Wet']
        for name in names:
            if request.POST.get(name) != None:
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
            'tags_json' : json.dumps(tags),
            'tags' : tags,
        }
        request.session['context'] = context
        return render(request, 'laundry_tag_check/result.html', context)

def judge_report(request):
    # file_name = request.session['file_url'].replace("/media/", "")
    file_name = request.session['file_url'].replace("/upload_img/", "")
    is_file = os.path.exists(MEDIA_ROOT + 'report/' + file_name)
    if is_file == False:
        shutil.copy( MEDIA_ROOT + file_name, MEDIA_ROOT + 'report/' + file_name)
        report = Report()
        report.image = 'report/' +  file_name
        report.ai_result = request.session['ai_result']
        report.user_result = request.session['tags']
        report.save()
        messages.success(request, '報告が完了しました。')
    else :
        messages.success(request, '報告済みです。')
    return render(request, 'laundry_tag_check/result.html', request.session['context'])

def report_admin(request):
    context=[]
    if  request.user.is_superuser :
        reports = Report.objects.all()
        context = {
            'message': 'report',
            "reports" : reports,
        }
        return render(request, 'report/index.html', context)
    else:
        context = {
        'ON' : json.dumps('home'),
        'message': 'Judge',
        'form': JudgeForm(),
        }
        return render(request, 'home/index.html', context)

def testYolo(request):
    # path_hubconfig = "yolo"
    # path_weightfile = "yolo/729x300_yolov5m_best.pt" 
    img_path = '/upload_img/0069.png'
    # model = torch.hub.load(path_hubconfig, 'custom',path=path_weightfile, source='local')
    results = MODEL(img_path.lstrip("/"))
    datas = json.loads(results.pandas().xyxy[0].to_json(orient="values"))
    tags=[]
    for data in datas :
        if data[4] > 0.5:
            tags.append(data[6]) 
    context = {
        'message': 'Test',
        'results': results,
        'xyxy': results.pandas().xyxy[0].to_json(orient="values"),
        'tags': tags,
        'datas': datas,
    }
    return render(request, 'testYolo/test.html', context)

