window.onload = function(){ 
    
    let checkbox = document.querySelectorAll("input[type='checkbox']");
    

    for (let i = 0; i < checkbox.length; i++) {
        checkbox[i].addEventListener('change', function() { //チェックボックス（type='checkbox'）の値が変更されたとき・・・ 
            let cbv = "'" + this.value + "'";  
            let checked = document.querySelectorAll("input[type='checkbox'][value =" + cbv + "]");

            if(this.checked){   
                for (let i = 0; i < checked.length; i++) {
                    checked[i].checked = true;
                }                                   //クリックされたチェックボックスがcheckedなら・・・
                let id = document.getElementsByClassName(this.value)
                for (let i = 0; i < id.length; i++) {
                    id[i].classList.replace('red', 'green');
                    id[i].innerText = ('済');
                }
            }
            else{
                for (let i = 0; i < checked.length; i++) {
                    checked[i].checked = false;
                } 
                let id = document.getElementsByClassName(this.value)
                for (let i = 0; i < id.length; i++) {
                    id[i].classList.replace('green', 'red');
                    id[i].innerText = ('未');
                }
            }
        });
    }
    
}