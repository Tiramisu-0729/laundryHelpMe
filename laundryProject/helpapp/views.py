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
        'message': '洗濯タグ判定 ',
        'user': user,
        'judage_form': JudgeForm(),
    }
    return render(request, 'home/index.html', context)
    
def washing_machine(request):
    context = {
        'message': '洗濯機',
    }
    return render(request, 'washing_machine/index.html',context)

def cabinet(request):
    context = {
        'message': 'タンス',
    }
    return render(request, 'cabinet/index.html', context)

def cabinet_form(request):
    user = request.user
    context = {
        'message': '追加',
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
            cabinet.image = request.FILES['image']#保存先はmyapp＞upload_img>imgのなか
            cabinet.save()
            context = {
                'message': '追加成功',
            }
        return render(request, 'cabinet/index.html', context)
    else:
        user = request.user
        context = {
            'message': '追加失敗',
            'user': user,
            'cabinet_form': CabinetForm(),
        }
    return render(request, 'cabinet/add.html', context)

    
def user(request):
    user = request.user
    context = {
        'message': 'ユーザー編集 ',
        'user': user,
    }
    return render(request, 'user/index.html', context)

def tips(request):
    return render(request, 'tips/index.html')

def judge(request):
    # if (request.method == 'POST'):
        # upload_image = cabinet(image=request.POST, request.FILES['image']) 画像だけとりたいpath入らない
    return render(request, 'washing_machine.html')
