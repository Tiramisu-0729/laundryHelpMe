window.onload = function(){ 
    
    let checkbox = document.querySelectorAll("input[type='checkbox']");
    let annotation =  document.getElementsByClassName("red");


    for (let i = 0; i < checkbox.length; i++) {
        checkbox[i].addEventListener('change', function() { //チェックボックス（type='checkbox'）の値が変更されたとき・・・ 
            if(this.checked){                                      //クリックされたチェックボックスがcheckedなら・・・
                annotation.classList.replace('green', 'red');
            }
            else{
                annotation.classList.replace('red', 'green');
            }
        });
    }
}