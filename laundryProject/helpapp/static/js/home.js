window.onload = function(){ 
    let id_img = document.getElementById('id_UploadImg');
    let submit = document.getElementById('submit');
    id_img.addEventListener('change', function() {
        //画像取得
        const img = id_img.files[0];
        home_img.setAttribute('src', "/static/pictures/img.png");
        submit.disabled = true;
        const type = img.type;
        //画像かどうかチェック
        if( !type.match(/^image/) ){
            alert('画像を選択してください');
            this.val('');
            return false;
        }

        //FileReaderオブジェクトのインスタンス化
        let reader = new FileReader();

        //画像の読み込み
        reader.readAsDataURL(img);

        //読み込み失敗時
        reader.onerror = function(){
            alert('ファイル読み取りに失敗しました');
            return false;
        }

        //画像を表示
        reader.onload = function() {
            home_img.setAttribute('src', reader.result);
            submit.disabled = false;
        }
        
    });
    submit.addEventListener('click', () => {
        var elements = document.getElementsByClassName('content');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "none";
            }
        var elements = document.getElementsByClassName('cssload-loadingwrap');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "flex";
            }
    });

}