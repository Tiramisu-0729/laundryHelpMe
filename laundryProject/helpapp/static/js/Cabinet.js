window.onload = function(){ 
    let edit = document.getElementById('edit');
    let check = document.getElementById('check');
    let content = document.getElementById('content');
    let checkbox = document.querySelectorAll("input[type='checkbox']");
    let btn = document.getElementsByClassName('btn')
    
  

    //チェックボックス表示切替
    edit.addEventListener('click', () => {  //editがクリックされたら
        check.classList.toggle('hidden');
        content.classList.toggle('hidden');
        if (edit.innerText == 'edit'){
            edit.innerText = 'cancel' ;
        }
        else{
            for (let i = 0; i < checkbox.length; i++) {
                checkbox[i].checked = false;
            }
            edit.innerText = 'edit' ;
        }
        
    });             
    
    for (let i = 0; i < checkbox.length; i++) {
        checkbox[i].addEventListener('change', function() { //チェックボックス（type='checkbox'）の値が変更されたとき・・・
            
            let check = document.form1.check;
            cnt = 0;
            arr=[];
            for (let i = 0; i < check.length; i++) {
                if (check[i].checked) {
                    arr.push(check[i].value);
                }
            }
            let newArr = Array.from(new Set(arr));
            //チェックボックスの同期
            let cbv = "'" + this.value + "'";   //クリックされたチェックボックスのvalue値を変数に格納
            let checked = document.querySelectorAll("input[type='checkbox'][value =" + cbv + "]");
            if(this.checked){                                      //クリックされたチェックボックスがcheckedなら・・・
                for (let i = 0; i < checked.length; i++) {
                    checked[i].checked = true;
                }
                if(btn[0].classList.contains('hidden')){
                    if(newArr.length > 0){
                        btn[0].classList.remove('hidden');
                    }
                }
                document.querySelector('#delete').value ='(' + newArr.length + ')' + '削除';
            }
            else{
                for (let i = 0; i < checked.length; i++) {
                    checked[i].checked = false;
                }
                i = newArr.length - 1;
                if(i == 0){
                    btn[0].classList.add('hidden');
                }
                document.querySelector('#delete').value ='(' + i + ')' + '削除';
            }
        });
    }
    
    
};

// カテゴリー変更 
function viewChange(){
    categories = ['all', 'tops', 'bottoms', 'outer', 'inner', 'other'];
    if(document.getElementById('categories')){
        id = document.getElementById('categories').value;
        for(let category of categories){
            if(id == category){
                var elements = document.getElementsByClassName(category);
                for(i=0;i<elements.length;i++){
                    elements[i].style.display = "";
                }
            }
            else{
                var elements = document.getElementsByClassName(category);
                for(i=0;i<elements.length;i++){
                    elements[i].style.display = "none";
                }
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





