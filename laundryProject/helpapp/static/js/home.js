$(function(){
    $('#id_UploadImg').change(function(){
        //画像取得
        const img = $('#id_UploadImg').prop('files')[0];
        home_img.setAttribute('src', "/static/pictures/img.png");
        const type = img.type;
        
        //画像かどうかチェック
        if( !type.match(/^image/) ){
            alert('画像を選択してください');
            $(this).val('');
            return false;
        }

        //FileReaderオブジェクトのインスタンス化
        let reader = new FileReader();

        //画像の読み込み
        reader.readAsDataURL(img);

        //読み込み失敗時
        reader.onerror = function(){
            alert('ファイル読み取りに失敗しました');
            $(this).val('');
            return false;
        }

        //画像を表示
        reader.onload = function() {
            home_img.setAttribute('src', reader.result);
        }

    });
})