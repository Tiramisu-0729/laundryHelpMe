window.onload = function(){ 
    let edit = document.getElementById('edit');
    let check = document.getElementById('check');
    let content = document.getElementById('content');
    
    let checkbox = document.querySelectorAll("input[type='checkbox']");
    let btn = document.getElementsByClassName('btn');
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
    
  

    //チェックボックス表示切替
    edit.addEventListener('click', () => {  //editがクリックされたら
        check.classList.toggle('hidden');
        content.classList.toggle('hidden');
        if (edit.innerText == '編集'){
            edit.innerText = '戻る' ;
        }
        else{
            for (let i = 0; i < checkbox.length; i++) {
                checkbox[i].checked = false;
            }
            edit.innerText = '編集' ;
        }
        
    });             
    

    for (let i = 0; i < checkbox.length; i++) {
        checkbox[i].addEventListener('change', function() { //チェックボックス（type='checkbox'）の値が変更されたとき・・・ 
            let check = document.form1.check;
            let arr=[];
            //チェックボックスの同期
            let cbv = "'" + this.value + "'";   //クリックされたチェックボックスのvalue値を変数に格納
            let checked = document.querySelectorAll("input[type='checkbox'][value =" + cbv + "]");
            if(this.checked){                                      //クリックされたチェックボックスがcheckedなら・・・
                for (let i = 0; i < checked.length; i++) {
                    checked[i].checked = true;
                }
                for (let i = 0; i < check.length; i++) {
                    if (check[i].checked) {
                        arr.push(check[i].value);
                    }
                }
                let newArr = Array.from(new Set(arr));
                if(btn[0].classList.contains('hidden')){
                    if(newArr.length > 0){
                        btn[0].classList.remove('hidden');
                        document.getElementById('add').style.bottom = "33vmin";
                    }
                }
                document.querySelector('#delete').value ='(' + newArr.length + ')' + '削除';
            }
            else{
                for (let i = 0; i < checked.length; i++) {
                    checked[i].checked = false;
                }
                for (let i = 0; i < check.length; i++) {
                    if (check[i].checked) {
                        arr.push(check[i].value);
                    }
                }
                let newArr = Array.from(new Set(arr));
                if(newArr.length == 0){
                    btn[0].classList.add('hidden');
                    document.getElementById('add').style.bottom = "20vmin";
                }
                document.querySelector('#delete').value ='(' + newArr.length + ')' + '削除';
            }
        });
    }
    let message = document.getElementById('success');
    message.addEventListener('click', () => { 
        message.classList.add('hidden');
    });
    
    
};









