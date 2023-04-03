let id = 1
let flag = 1

function GetSelectOption () {
    let button = document.getElementById('btn')
    button.disabled = true;
};

function AddCadastralNumber() {
    GetSelectOption();
    UndisabledButton();
    let cadatral_number = document.getElementById('id_cadastral_number')
    let div = document.createElement("div")
    div.style.cssText = 'display:flex;'
    div.className='input-group'
    div.innerHTML = `<input id='cadastral_number${id}' type='text' name='cadastral_numbers' class='form-control' readonly value='${cadatral_number.value}' style='border-radius:8px; text-align:center;'>
    <button id='edit' type='button' onClick='EditCadastral(cadastral_number${id})' style='margin:auto 5px auto 5px;'><i class='bx bxs-edit btn btn-outline-secondary'></i></button>
    <button id='delete' type='button' onClick='DeleteCadastral(cadastral_number${id});'><i class='bx bxs-x-circle btn btn-outline-secondary'></i></button>`

    my_div = document.getElementById("cadastal_numbers");
    my_div.parentNode.insertBefore(div, my_div)

    cadatral_number.value=''
    id ++;
};

function UndisabledButton() {
    document.getElementById('order-btn').disabled = false;
}

function DeleteCadastral(cadastral_number) {
    document.getElementById('edit').remove();
    document.getElementById('delete').remove();
    document.getElementById(cadastral_number.id).remove()
}

function EditCadastral(cadastral_number) {
    let cadastral = document.getElementById(cadastral_number.id);
    let edit = document.getElementById('edit')
    if (flag) {
        edit.innerHTML = "<i class='bx bxs-check-circle btn btn-outline-secondary'></i>";
        cadastral.readOnly = false;
        cadastral.style.cssText = 'background-color:lightgray';
        flag--;
    }
    else {
        edit.innerHTML = "<i class='bx bxs-edit btn btn-outline-secondary'></i>";
        cadastral.readOnly = true;
        alert(cadastral.value)
        cadastral.style.cssText = 'border-radius:8px; text-align:center;'
        flag++;
    }
}

