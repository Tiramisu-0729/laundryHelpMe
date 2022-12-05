
$(function(){
    $('#id_image').change(function(){
        //画像取得
        const img = $('#id_image').prop('files')[0];
        image.setAttribute('src', "/static/pictures/img.png");
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
            image.setAttribute('src', reader.result);
        }
        
    });
    const submit = document.getElementById('submit');
    submit.addEventListener('click', () => {
        var elements = document.getElementsByClassName('content');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "none";
            }
        var elements = document.getElementsByClassName('loading');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "flex";
            }
    });

})