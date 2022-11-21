window.onload = function(){ 
    const edit = document.getElementById('edit');
    const check = document.getElementById('check');
    const content = document.getElementById('content');

    //チェックボックス表示切替
    edit.addEventListener('click', () => {
        check.classList.toggle('hidden');
        content.classList.toggle('hidden');
    });

    //form送信先設定
    // let button = document.getElementById('btn');
    $('.submit').click(function() {
        $(this).parents().parents('form').attr('action', $(this).data('action'));
        $(this).parents().parents('form').submit();
    });
};

var ref = document.referrer
if (ref.indexOf('helpapp/cabinet_form') !== -1) {
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

