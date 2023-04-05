let id = 1
let flag = 1
let array = []

function GetSelectOption () {
    let button = document.getElementById('btn')
    button.disabled = true;
};

function AddCadastralNumber() {
    GetSelectOption();
    UndisabledButton();
    let cadatral_number = document.getElementById('id_cadastral_number')
    if (array.includes(cadatral_number.value) == false) {
        array.push(cadatral_number.value);
        let div = document.createElement("div");
        div.style.cssText = 'display:flex;';
        div.className='input-group';
        div.id = id;
        div.innerHTML = `<input id='cadastral_number${id}' type='text' name='cadastral_numbers' class='form-control' onchange='VaidateCadastral(${id});' readonly value='${cadatral_number.value}' style='border-radius:8px; text-align:center;'>
        <button id='edit${id}' type='button' onClick='EditCadastral(${id})' style='margin:auto 5px auto 5px;'><i class='bx bxs-edit btn btn-outline-secondary'></i></button>
        <button id='delete' type='button' onClick='DeleteCadastral(${id});'><i class='bx bxs-x-circle btn btn-outline-secondary'></i></button>`
    
        my_div = document.getElementById("cadastal_numbers");
        my_div.parentNode.insertBefore(div, my_div);
        cadatral_number.value='';
        id ++;
    }
    else {
        alert('Данный кадастровый номер уже добавлен')
    }
};

function UndisabledButton() {
    document.getElementById('order-btn').disabled = false;
}

function DeleteCadastral(id) {
    let cadastral_number = document.getElementById(`cadastral_number${id}`);
    let index = array.indexOf(cadastral_number.value);
    document.getElementById(id).remove();
    array.splice(index, 1);
}


function EditCadastral(id) {
    let cadastral = document.getElementById(`cadastral_number${id}`);
    let edit = document.getElementById(`edit${id}`)
    if (flag) {
        edit.innerHTML = "<i class='bx bxs-check-circle btn btn-outline-secondary'></i>";
        cadastral.readOnly = false;
        cadastral.style.cssText = 'background-color:lightgray';
        flag--;
    }
    else {
        let [a, new_cadastral] = VaidateCadastral(id);
        if (a) {
            edit.innerHTML = "<i class='bx bxs-edit btn btn-outline-secondary'></i>";
            cadastral.readOnly = true;
            cadastral.style.cssText = 'border-radius:8px; text-align:center;'
            let index = array.indexOf(cadastral.value);
            array.splice(index);
            array.push(new_cadastral);
            flag++;
        }
    }
}

function VaidateCadastral(id) {
    let cadastral = document.getElementById(`cadastral_number${id}`);
    if (array.includes(cadastral.value)) {
        alert('Данный кадастровый номер уже добавлен')
        document.getElementById(`cadastral_number${id}`).value = cadastral.value

        return false
    }
    else {
        return [true, cadastral.value]
    }
}