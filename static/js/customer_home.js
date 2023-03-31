function GetSelectOption () {
    let cadastral_number = document.getElementById("id_cadastral_number");
    let option = document.createElement('option');
    let button = document.getElementById('btn')
    button.disabled = true;
    option.text = cadastral_number.value;
    option.selected = true;
    document.querySelector('#select').add(option);
};

function AddCadastralNumber() {
    GetSelectOption();
    select.style.cssText = 'display:block; overflow:hidden';
    document.getElementById('id_cadastral_number').value = ''
    
};