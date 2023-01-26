
window.onload = function(){ 
    document.querySelector('[for="id_image"]').innerHTML ="<img id='image' src='{% static 'pictures/img.png' %}' alt=''>";
    document.querySelector('[for="id_name"]').innerText = 'NAME';
    document.querySelector('[for="id_category"]').innerText = 'CATEGORY';
    document.querySelector('[for="id_memo"]').innerText = 'MEMO';
    document.querySelector('[for="id_memo"]').style.float="left";
    document.querySelector('[for="id_category"]').style.float="left";
    document.querySelector('[for="id_name"]').style.float="left";
    document.getElementById("id_name").maxLength = 20;
    let img = document.querySelector('input[type="file"]');
    img.required = true;
    let id_img = document.getElementById('id_image');


    id_img.addEventListener('change', function() {
        
        //画像取得
        const img = id_img.files[0];

        image.setAttribute('src', "/static/pictures/img.png");
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
            image.setAttribute('src', reader.result);
        }
        
    });
}