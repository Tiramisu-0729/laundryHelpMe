window.onload = function(){ 
    let buttons = document.getElementsByClassName("edit-button");
    let edit = document.getElementById("edit");
    let main = document.getElementById("main");
    let id_img = document.getElementById('file');   

    id_img.addEventListener('change', function () {
        //画像取得
        let img = id_img.files[0];
        let type = img.type;
        //画像かどうかチェック
        if (!type.match(/^image/)) {
            alert('画像を選択してください');
            this.val('');
            return false;
        }

        //FileReaderオブジェクトのインスタンス化
        let reader = new FileReader();

        //画像の読み込み
        reader.readAsDataURL(img);

        //読み込み失敗時
        reader.onerror = function () {
            alert('ファイル読み取りに失敗しました');
            return false;
        }

        //画像を表示
        reader.onload = function () {
            upload_img.setAttribute('src', reader.result);
        }

    });
    submit.addEventListener('click', () => {
        var elements = document.getElementsByClassName('content');
        for (i = 0; i < elements.length; i++) {
            elements[i].style.display = "none";
        }
        var elements = document.getElementsByClassName('load');
        for (i = 0; i < elements.length; i++) {
            elements[i].style.display = "block";
        }
    });




    for (let button of buttons)
        button.addEventListener('click', () => {  //editがクリックされたら
            edit.classList.toggle('hidden');
            main.classList.toggle('hidden');

        });




    //ラジオボタン消せるようにする
    const radioBtns = Array.prototype.slice.call(document.querySelectorAll('input[type="radio"]'), 0);
    //ラジオボタンが存在する場合は処理する
    if (radioBtns.length !== 0) {
        //ラジオボタンごとの設定
        radioBtns.forEach(function (radioBtn, index) {
            //ラジオボタン識別番号設定
            radioBtn.radioIndex = index;
            //チェックフラグ設定
            if (radioBtn.checked) {
                radioBtn.checkFlg = true;
            } else {
                radioBtn.checkFlg = false;
            }
            //クリックイベント設定
            radioBtn.addEventListener('click', function () {
                //番号を取得
                const thisIndex = this.radioIndex;
                //同じグループのラジオボタンを取得
                const group = Array.prototype.slice.call(document.querySelectorAll('input[type="radio"][name="' + radioBtn.name + '"]'), 0);
                //未チェックの場合
                if (!this.checkFlg) {
                    //チェックフラグオン（checkedはJSで書かずともtrueになるので省略）
                    this.checkFlg = true;
                    //チェックした要素以外のフラグをfalseに
                    group.forEach(function (elm) {
                        if (elm.checkFlg && elm.radioIndex !== thisIndex) {
                            elm.checkFlg = false;
                        }
                    });
                } else {
                    //既にチェックしている場合（リセット処理）
                    group.forEach(function (elm) {
                        //チェックフラグがtrueかつ識別番号が一致するradio要素
                        if (elm.checkFlg && elm.radioIndex === thisIndex) {
                            //チェックフラグfalse
                            elm.checkFlg = false;
                            //ラジオボタンのチェック解除
                            elm.checked = false;
                        }
                    });
                }
            });
        });
    }
}
