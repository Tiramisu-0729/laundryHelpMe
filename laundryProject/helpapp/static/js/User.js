window.onload = function(){ 
    
    let edit = document.getElementById('edit-button');
    let main = document.getElementById('main');
    let main_edit = document.getElementById('main_edit');

    edit.addEventListener('click', () => {  //editがクリックされたら
        main.classList.toggle('hidden');
        main_edit.classList.toggle('hidden');
        if (edit.innerText == '編集'){
            edit.innerText = '戻る' ;
        }
        else{
            edit.innerText = '編集' ;
        }
    });
    let id_img = document.getElementById('id_image');
    id_img.addEventListener('change', function() {
        //画像取得
        let img = id_img.files[0];
        //image.setAttribute('src', "/static/pictures/img.png");
        let type = img.type;
        
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
            account_img.setAttribute('src', reader.result);
        }
        
    });
}