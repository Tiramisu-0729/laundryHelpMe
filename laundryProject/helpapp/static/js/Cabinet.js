window.onload = function(){ 
    const edit = document.getElementById('edit');
    const check = document.getElementById('check');
    const content = document.getElementById('content');
    var title = document.getElementById("title");
  

    //チェックボックス表示切替
    edit.addEventListener('click', () => {
        check.classList.toggle('hidden');
        content.classList.toggle('hidden');
        // if (title.innerHTML === "Cabinet") {
        //     title.innerHTML = "Edit";
        // } else {
        //     title.innerHTML = "Cabinet";
        // }
    });


    //form送信先設定
    $('.submit').click(function() {
        $(this).parents().parents('form').attr('action', $(this).data('action'));
        $(this).parents().parents('form').submit();
    });

    //チェックボックスの同期
    $("input[type='checkbox']").on('change', function(){                 //チェックボックス（type='checkbox'）の値が変更されたとき・・・
        cbv = $(this).val();                                               //クリックされたチェックボックスのvalue値を変数に格納
        if( $(this).prop('checked')){                                      //もしクリックされたチェックボックスがチェックされていたら・・・
            $("input:checkbox[value='" + cbv + "']").prop('checked',true);   //同じvalueを持つチェックボックスは全部チェックを入れる
        }
        else{
            $("input:checkbox[value='" + cbv + "']").prop('checked',false);  //逆にチェックが外れていたら全部チェックを外す。
        }
    });
};

// カテゴリー変更   allは出たけどTOPS出なかった
function viewChange(){
    if(document.getElementById('categories')){
        id = document.getElementById('categories').value;
        if(id == 'all'){
            var elements = document.getElementsByClassName('all');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "";
            }
            var elements = document.getElementsByClassName('tops');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "none";
            }
            var elements = document.getElementsByClassName('bottoms');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "none";
            }
            var elements = document.getElementsByClassName('outer');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "none";
            }
            var elements = document.getElementsByClassName('inner');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "none";
            }
            var elements = document.getElementsByClassName('other');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "none";
            }
        }
        else if(id == 'tops'){
            var elements = document.getElementsByClassName('all');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "none";
            }
            var elements = document.getElementsByClassName('tops');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "";
            }
            var elements = document.getElementsByClassName('bottoms');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "none";
            }
            var elements = document.getElementsByClassName('outer');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "none";
            }
            var elements = document.getElementsByClassName('inner');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "none";
            }
            var elements = document.getElementsByClassName('other');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "none";
            }
        }
        else if(id == 'bottoms'){
            var elements = document.getElementsByClassName('all');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "none";
            }
            var elements = document.getElementsByClassName('tops');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "none";
            }
            var elements = document.getElementsByClassName('bottoms');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "";
            }
            var elements = document.getElementsByClassName('outer');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "none";
            }
            var elements = document.getElementsByClassName('inner');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "none";
            }
            var elements = document.getElementsByClassName('other');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "none";
            }
        }
        else if(id == 'outer'){
            var elements = document.getElementsByClassName('all');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "none";
            }
            var elements = document.getElementsByClassName('tops');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "none";
            }
            var elements = document.getElementsByClassName('bottoms');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "none";
            }
            var elements = document.getElementsByClassName('outer');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "";
            }
            var elements = document.getElementsByClassName('inner');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "none";
            }
            var elements = document.getElementsByClassName('other');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "none";
            }
        }
        else if(id == 'inner'){
            var elements = document.getElementsByClassName('all');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "none";
            }
            var elements = document.getElementsByClassName('tops');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "none";
            }
            var elements = document.getElementsByClassName('bottoms');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "none";
            }
            var elements = document.getElementsByClassName('outer');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "none";
            }
            var elements = document.getElementsByClassName('inner');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "";
            }
            var elements = document.getElementsByClassName('other');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "none";
            }
        }
        else if(id == 'other'){
            var elements = document.getElementsByClassName('all');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "none";
            }
            var elements = document.getElementsByClassName('tops');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "none";
            }
            var elements = document.getElementsByClassName('bottoms');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "none";
            }
            var elements = document.getElementsByClassName('outer');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "none";
            }
            var elements = document.getElementsByClassName('inner');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "none";
            }
            var elements = document.getElementsByClassName('other');
            for(i=0;i<elements.length;i++){
                elements[i].style.display = "";
            }
        }
    }

window.onload = viewChange;
}

// メッセージ
var ref = document.referrer
if (ref.indexOf('helpapp/cabinet_add') !== -1) {
    alert("保存しました");
    history.pushState(null, null, location.href);
    window.addEventListener('popstate', (e) => {
        history.go(1);
    });
} 

else if (ref.indexOf('helpapp/cabinet_detele/*') !== -1) {
    alert("削除しました");
    history.pushState(null, null, location.href);
    window.addEventListener('popstate', (e) => {
        history.go(1);
    });
}
else if (ref.indexOf('helpapp/cabinets_detele') !== -1) {
    alert("削除しました");
    history.pushState(null, null, location.href);
    window.addEventListener('popstate', (e) => {
        history.go(1);
    });
}

