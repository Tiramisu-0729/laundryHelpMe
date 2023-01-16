window.onload = function(){ 
    let edit = document.getElementById('edit');
    let check = document.getElementById('check');
    let content = document.getElementById('content');
    
    let checkbox = document.querySelectorAll("input[type='checkbox']");
    let btn = document.getElementsByClassName('btn');
    let space = document.getElementsByClassName('space');
  

    //チェックボックス表示切替
    edit.addEventListener('click', () => {  //editがクリックされたら
        check.classList.toggle('hidden');
        content.classList.toggle('hidden');
        if (edit.innerText == '編集'){
            edit.innerText = '戻る' ;
            btn[0].classList.add('hidden');
            space[0].style.margin = "20vmin";
            document.getElementById('add').style.bottom = "20vmin";
        }
        else{
            for (let i = 0; i < checkbox.length; i++) {
                checkbox[i].checked = false;
            }
            edit.innerText = '編集' ;
            btn[0].classList.add('hidden');
            space[0].style.margin = "20vmin";
            document.getElementById('add').style.bottom = "20vmin";
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
                        space[0].style.margin = "35vmin";
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
                    space[0].style.margin = "20vmin";
                    document.getElementById('add').style.bottom = "20vmin";
                }
                document.querySelector('#delete').value ='(' + newArr.length + ')' + '削除';
            }
        });
    }

};









