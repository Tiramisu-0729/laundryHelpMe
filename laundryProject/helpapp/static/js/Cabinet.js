window.onload = function(){ 
    const edit = document.getElementById('edit');
    const check = document.getElementById('check');
    const content = document.getElementById('content');
  

    //チェックボックス表示切替
    edit.addEventListener('click', () => {  //editがクリックされたら
        check.classList.toggle('hidden');
        content.classList.toggle('hidden');
        if (edit.innerText == 'edit'){
            edit.innerText = 'cancel' ;
        }
        else{
            edit.innerText = 'edit' ;
        }
        
    });

    
    $("input[type='checkbox']").on('change', function(){                 //チェックボックス（type='checkbox'）の値が変更されたとき・・・
        const check = document.form1.check;
        cnt = 0;
        arr=[];
        for (let i = 0; i < check.length; i++) {
            if (check[i].checked) {
                arr.push(check[i].value);
            }
        }
        const newArr = Array.from(new Set(arr));
        

        //チェックボックスの同期
        cbv = $(this).val();                                               //クリックされたチェックボックスのvalue値を変数に格納


        if( $(this).prop('checked')){                                      //もしクリックされたチェックボックスがチェックされていたら・・・
            $("input:checkbox[value='" + cbv + "']").prop('checked',true);   //同じvalueを持つチェックボックスは全部チェックを入れる
            document.querySelector('#delete').value ='(' + newArr.length + ')' + '削除';
        }
        else{
            i = newArr.length - 1;
            $("input:checkbox[value='" + cbv + "']").prop('checked',false);  //逆にチェックが外れていたら全部チェックを外す。
            document.querySelector('#delete').value ='(' + i + ')' + '削除';
        }
    });
};

// カテゴリー変更 
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

