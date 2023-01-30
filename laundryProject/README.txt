管理者サイトのあれこれ。

・アノテーション
    3列目のURLを押下、画像をダウンロードする
    ユーザーの判定などをもとにアノテーションする
    アノテーション列の該当行を押下し、完了にする
    表右上の保存するボタンを押す
    ローカルのYoloV5で追加学習させる
    重みファイルはサーバーの「/home/opc/laundryProject/yolo/729x300_yolov5m_best.pt」


### サーバー設定
# サーバー再起動
sudo systemctl restart project

# StaticファイルをSTATIC_ROOTにあつめる
sudo python3.7 manage.py collectstatic

#プロジェクト起動サービス設定(Gunicorn)
sudo vim /etc/systemd/system/project.service

# nginxの設定ファイル
/etc/nginx/conf.d/laundryhelpme.0g0.jp.conf

#作らなきゃいけないフォルダ
usr/share/nginx/html/media/icon/
usr/share/nginx/html/media/img/
usr/share/nginx/html/media/report/

# 自動更新系 
sudo crontab -l　#このコマンドで確認できる
# nginx -> ウェブ証明書自動更新 毎月1日、15日の1時10分更新
10 1 1,15 * * certbot renew --pre-hook "systemctl stop nginx" --post-hook "systemctl start nginx"

# mydns -> mydnsの自動ログイン
0 1 * * * curl -u ユーザー名:パスワード https://www.mydns.jp/login.html

# tmpwatch -> 毎時0分に作成から12時間過ぎたファイルを削除
0 * * * * tmpwatch -m 24 -d /usr/share/nginx/html/media/ -x /usr/share/nginx/html/media/icon/ -x /usr/share/nginx/html/media/img/ -x /usr/share/nginx/html/media/report/

# Let'ｓ Encrypt証明書の場所
/etc/letsencrypt/live/laundryhelpme.0g0.jp/


#/report/index.htmlのサーバーとローカルで変えるとこ
{% with img="/upload_img/"|add:report.image %}　#ローカル
↓
{% with img="/media/"|add:report.image %} #サーバー

#ローカルとサーバーでパス等が違うところがあるのでサーバー用バックアップ部分
def judge(request):
    try :
        if request.method == "POST":
            image = request.FILES['UploadImg']#保存先はmediaのなか　いったん保存
            fs = FileSystemStorage()
            ext = os.path.splitext(image.name)
            file_data = fs.save(request.user.username + ext[1], image)
            file_url = fs.url(file_data)
            request.session['file_url'] = file_url
            #AIで画像判定
            results = MODEL('/usr/share/nginx/html'+file_url) # model_loadからMODEL読み込み
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
    except :
        messages.success(request, 'エラーが発生しました')    
    return redirect('/helpapp/home')

def judge_report(request):
    if request.user.is_authenticated :
        file_name = request.session['file_url'].replace("/media/", "")
        is_file = os.path.exists(MEDIA_ROOT + '/report/' + file_name)
        if is_file == False:
            shutil.copy( MEDIA_ROOT + '/' + file_name, MEDIA_ROOT + '/report/' + file_name)
            report = Report()
            report.image = 'report/' +  file_name
            report.ai_result = request.session['ai_result']
            report.user_result = request.session['tags']
            report.save()
            messages.success(request, '報告が完了しました。')
        else :
            messages.success(request, '報告済みです。')
        return render(request, 'laundry_tag_check/result.html', request.session['context'])
    else :
        return redirect('/accounts/login/')
