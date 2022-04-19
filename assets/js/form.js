user = ""

// FORM BUILDING
//#region 
async function retrieveForm(formName) {

    var serviceURL = "http://127.0.0.1:5003/formbuilder/" + formName;

    try {
        // Retrieve list of all fields
        const response =
            await fetch(
                serviceURL, {
                    method: 'GET'
                }
            );
        const result = await response.json();
        if (response.ok) {
            // success case
            var allFields = result.data.items;
            for (field of allFields) {
                if (field.fieldType == "radio") {
                    buildRadio(field);
                }
                if (field.fieldType == "text") {
                    buildText(field);
                }
                if (field.fieldType == "checkbox") {
                    buildCheckbox(field);
                }
                if (field.fieldType == "file") {
                    buildFile(field);
                }
                if (field.fieldType == "dropdown") {
                    buildDropdown(field);
                }
                if (field.fieldType == "number") {
                    buildNumber(field);
                }
            }


            // if edit page --> change as needed
            if ($('body').is('.editForm')) {
                addIcons(formName);
            }

            // compulsory fields
            var readonly = "";
            if (formName == "wishlist") {
                readonly = "readonly";
            }
            // console.log(user.username)
            var contactField = `<label for="contactNo" class="form-label">Contact Number</label>
            
                                <input required type="number" ${readonly} class="form-control" value=${user.username} id="contactNo" name="contactNo">`

            var itemNameField = `<!--On change of this dropdown, auto get item names listed under this category-->
                                <div class="col-md-6">
                                    <label for="itemCategoryOptions" class="form-label">Item Category</label>
                                    <select onchange="populateSubCat(this)" class="form-select" id="itemCategoryOptions" name="category"
                                        required>
                                        <!--Dynamically dropdown categories listed in existing db-->
                                    </select>
                                </div>`

            var subCatField = `<div class="col-md-6">
                                    <label for="subCatOptions" class="form-label">Sub-Category</label>
                                    <select onchange="populateItemNames(this)" class="form-select" id="subCatOptions" name="subcat"
                                        required>
                                        <!--Dynamically dropdown subcats listed in existing db-->
                                    </select>
                                </div>`

            var catField = `<!--Option value for item name needs to be dynamic, based on category-->
                                <div class="col-md-6">
                                    <label for="itemNameOptions" class="form-label">Item Name</label>
                                    <select class="form-select" id="itemNameOptions" name="itemName" required>
                                        <!--Dynamically update item names-->
                                    </select>
                                </div>`;

            document.getElementById('contactField').innerHTML += contactField;
            document.getElementById(formName).innerHTML += itemNameField + subCatField + catField;
        }
    } catch (error) {
        // Errors when calling the service; such as network error, 
        // service offline, etc
        console.log(error)
        alert('There is a problem retrieving data, please refresh the page or try again later.');
    } // error
}

function buildRadio(field) {

    var radioField = `
            <div class="col-md-6">
              <label for="${field.fieldID}" class="form-label">${field.fieldName}</label>
              <br>`;

    var options = field.options.split(";");

    for (var option of options) {
        radioField +=
            `<label class="radio-inline" style="padding-right: 7px;" >
                        <input required class="form-check-input" type="radio" name="${field.fieldID}" value="${option}"> ${option}
                    </label>`;
    }

    radioField += `</div>`;

    document.getElementById(field.formName).innerHTML += radioField;
}

function buildText(field) {
    var textField = `<div class="col-md-6">
                        <label for="${field.fieldID}" class="form-label">${field.fieldName}</label>
                        <input required type="text" class="form-control" name="${field.fieldID}" id="${field.fieldID}" placeholder="${field.placeholder ?? ""}">
                    </div>`;


    document.getElementById(field.formName).innerHTML += textField;
}

function buildNumber(field) {
    var numField = `<div class="col-md-6">
                        <label for="${field.fieldID}" class="form-label">${field.fieldName}</label>
                        <input required type="number" class="form-control" name="${field.fieldID}" id="${field.fieldID}" placeholder="${field.placeholder ?? ""}">
                    </div>`;


    document.getElementById(field.formName).innerHTML += numField;
}

function buildFile(field) {
    var fileField = `<div class="col-md-6">
                        <div class="form-group">
                            <label for="${field.fieldID}" class="form-label">${field.fieldName}</label>
                            <input required type="file" name="${field.fieldID}" class="form-control" id="${field.fieldID}" style="display:block">
                        </div>
                    </div>`;

    document.getElementById(field.formName).innerHTML += fileField;
}

function buildDropdown(field) {
    var dropdownField = `
            <div class="col-md-6">
              <label for="${field.fieldID}" class="form-label">${field.fieldName}</label>
              <select required class="form-select" id="${field.fieldID}" name="${field.fieldID}">`;

    if (field.options !== null) {
        var options = field.options.split(";");
        for (var option of options) {
            dropdownField += `<option value="${option}"> ${option}</option>`;
        }
    }

    dropdownField += `</select></div>`;

    document.getElementById(field.formName).innerHTML += dropdownField;
}

function buildCheckbox(field) {

    var checkboxField = `
            <div class="col-md-6">
              <label for="${field.fieldID}" class="form-label">${field.fieldName}</label>
              <br>`;

    var options = field.options.split(";");

    var optionNo = 1;
    for (var option of options) {
        checkboxField +=
            `<input id="${field.fieldID}-${optionNo}" class="form-check-input" type="checkbox" name="${field.fieldID}" value="${option}">
                    <label for="${field.fieldID}-${optionNo}" class="form-check-inline" style="padding-right: 7px;" >${option}</label>`;
        optionNo++;
    }

    checkboxField += `</div>`;

    document.getElementById(field.formName).innerHTML += checkboxField;
}

// add edit icons to each field
function addIcons(formName) {
    $(`#${formName}`).find('input, select').each(function () {
        var fieldID = $(this).attr("name");
        if (fieldID === undefined) {
            fieldID = $(this).attr("id");
        }
        var editIcon = ` <i type="button" onclick="editField(${fieldID})" class="bi bi-pencil m-1" style="font-size:14px"></i>`;
        var label = $(`label[for="${fieldID}"]`);
        if (!label.next().is("i")) {
            label.after(editIcon);
        }
    });
};
//#endregion

// POPULATING ITEM CATEGORIES, SUB-CATEGORIES AND NAMES DROPDOWN LISTS
//#region
function populateCategoryItems() {

    getDropDownCat().then(function autoPopCategories(result) {
        var catList = result

        // reset dropdown fields
        $('#itemCategoryOptions').html("")
        $('#itemNameOptions').html("")
        $('#subCatOptions').html("")

        // Start off with an empty selected option for category
        $('#itemCategoryOptions').append(`<option disabled selected> </option>`)
        $('#subCatOptions').append("<option disabled selected> Please select a category first </option>")
        $('#itemNameOptions').append("<option disabled selected> Please select a sub-category first </option>")

        for (cat of catList) {
            $('#itemCategoryOptions').append(`
                <option value="${cat}">${cat}</option>
            `)
        }
    })
    var catalogTable = document.getElementById('catalogTable')
    getCatalog().then(function populateCatalog(result) {
        var catalogList = result

        // reset catalog on refresh
        catalogTable.innerHTML = `<tr>
                                <th>Category</th>
                                <th>Sub-Category</th>
                                <th>Item Name</th>
                            </tr>`

        for (ele in catalogList) {
            catalogTable.innerHTML += `
            <tr>
                <td>${catalogList[ele].category}</td>
                <td>${catalogList[ele].subCat}</td>
                <td>${catalogList[ele].itemName}</td>
            </tr>
            `
        }
    })

}

async function getCatalog() {
    let response = await fetch("http://127.0.0.1:5003/getCatalog")
    let res = await response.json()

    if (res.code == 200) {
        return res.items
    } else {
        alert(res.message)
    }
}

async function getDropDownCat() {
    let response = await fetch("http://127.0.0.1:5003/getCat")
    let responseCode = await response.json()

    if (responseCode.code == 200) {
        return responseCode.data.categories
    } else {
        alert(responseCode.message)
    }
}

async function populateSubCat(cat) {
    $('#subCatOptions').html("")
    cat = cat.value
    let response = await fetch("http://127.0.0.1:5003/getSubCat/" + cat)
    let responseCode = await response.json()

    if (responseCode.code == 200) {
        $('#subCatOptions').append("<option disabled selected> </option>")
        let subCatArr = []
        for (subcat of responseCode.data.subcats) {
            if (!subCatArr.includes(subcat.subCat)) {
                subCatArr.push(subcat.subCat)
            }
        }
        for (sub of subCatArr) {
            $('#subCatOptions').append(`<option value="${sub}">${sub}</option>`)
        }
    }
}

async function populateItemNames(cat) {
    $('#itemNameOptions').html("")
    cat = cat.value
    subcat = document.getElementById("itemCategoryOptions").value;
    let response = await fetch("http://127.0.0.1:5003/getItemNames/" + subcat + "/" + cat)
    let responseCode = await response.json()
    if (responseCode.code == 200) {
        $('#itemNameOptions').append("<option disabled selected> </option>")
        for (cat of responseCode.data.itemsInCat) {
            $('#itemNameOptions').append(`<option value="${cat.itemID}">${cat.itemName}</option>`)
        }
    }
}
//#endregion

// DISPLAYING EDITING FORM
//#region 
function showFieldType() {
    var inputType = $("#fieldType :selected").val();
    if (inputType == "text" || inputType == "number") {
        if ($('#textInput').length == 0) {
            $('#newField').append(`<div id="textInput">
                                    <input type="text" class="form-control" id="placeholder" placeholder="Enter placeholder text here (optional)">
                                </div>`);
        }
        $('#addOptions').hide();
        $('#textInput').show();
    } else if (inputType == "radio" || inputType == "dropdown" || inputType == "checkbox") {
        if ($('#addOptions').length == 0) {
            $('#newField').append(`<div id="addOptions"><ol id="optionsList"></ol></div>`)
            addOption();
            $('#addOptions').append(`<button class="btn btn-outline-secondary ms-3" type='button' id="addOptionBtn"
                                    onclick="addOption()">+ Add Option</button>`);
        }
        $('#textInput').hide();
        $('#addOptions').show();
    } else {
        $('#textInput').hide();
        $('#addOptions').hide();
    }
}

function addOption(value = "") {
    var option = `<li><div class="input-group">
                        <input type="text" class="form-control mb-3" ${value} name="option" placeholder="Enter new option">
                        <button type="button" onclick="removeOption(this)" class="btn-close m-2" aria-label="Close"></button>
                    </div></li>`;
    $('#optionsList').append(option);
}

function removeOption(elem) {
    elem.parentNode.parentNode.remove();
}
//#endregion

// FIELD CUD
//#region 
async function addField(formName, fieldID = "") {
    var fieldName = $('#fieldName').val();
    var fieldType = $('#fieldType').val();
    if (fieldType == "text" || fieldType == "number") {
        var placeholder = $('#placeholder').val();
        var fieldData = JSON.stringify({
            formName: formName,
            fieldName: fieldName,
            fieldType: fieldType,
            placeholder: placeholder
        })
    } else if (fieldType == "radio" || fieldType == "dropdown" || fieldType == "checkbox") {
        var options = '';
        $("[name='option']").each(function () {
            options += this.value + ';';
        });
        options = options.slice(0, -1);
        var fieldData = JSON.stringify({
            formName: formName,
            fieldName: fieldName,
            fieldType: fieldType,
            options: options
        })
    } else {
        var fieldData = JSON.stringify({
            formName: formName,
            fieldName: fieldName,
            fieldType: fieldType
        })
    }

    var serviceURL = "http://127.0.0.1:5003/formbuilder" + fieldID;

    return fetch(serviceURL, {
            method: "POST",
            headers: {
                "Content-type": "application/json"
            },
            body: fieldData
        })
        .then(response => response.json())
        .then(data => {
            // console.log(data);
            window.location = window.location;
        })
};

async function editField(fieldID) {
    var serviceURL = "http://127.0.0.1:5003/formbuilder/" + fieldID;

    try {
        // Retrieve list of all FAQ
        const response =
            await fetch(
                serviceURL, {
                    method: 'GET'
                }
            );
        const result = await response.json();
        if (response.ok) {
            var field = result.data;
            $('#fieldName').val(field.fieldName);
            $('#fieldType').val(field.fieldType);

            if (field.placeholder !== null) {
                // resets placeholder field
                if ($('#textInput').length != 0) {
                    $('#textInput').remove()
                }

                // build placeholder field
                $('#newField').append(`<div id="textInput">
                                    <input type="text" class="form-control" id="placeholder" placeholder="Enter placeholder text here (optional)">
                                </div>`);
                $('#placeholder').val(field.placeholder);
            }

            if (field.options !== null) {
                // resets options fields
                if ($('#addOptions').length != 0) {
                    $('#addOptions').remove()
                }

                // build options fields
                $('#newField').append(`<div id="addOptions"><ol id="optionsList"></ol></div>`);
                var options = field.options.split(";");
                for (var option of options) {
                    addOption(`value="${option}"`);
                }
                $('#addOptions').append(`<button class="btn btn-outline-secondary ms-3" type='button' id="addOptionBtn"
                                    onclick="addOption()">+ Add Option</button>`)
            }

            showFieldType();
            if ($('#deleteFieldBtn').length == 0) {
                $('#editHeader').append(`<div class="col-md-6">
                                        <button type="button" class="btn btn-danger float-end" id="deleteFieldBtn">Delete Field</button>
                                    </div>`);
                $('#addFieldBtn').text("Save Changes");
                $('#editField').html("Edit Field");
            }

            $('#deleteFieldBtn').attr("onclick", `deleteField(${field.fieldID})`);
            $('#addFieldBtn').attr("onclick", `addField('${field.formName}', '/${field.fieldID}')`);
            document.getElementById('editField').scrollIntoView();
        }
    } catch (error) {
        // Errors when calling the service; such as network error, 
        // service offline, etc
        console.log(error)
        alert('There is a problem retrieving data, please refresh the page or try again later.');
    } // error
}

async function deleteField(fieldID) {
    if (confirm("Are you sure you want to delete this field? This will also delete all data related to the field.")) {
        var serviceURL = "http://127.0.0.1:5003/formbuilder/" + fieldID;

        try {
            // Retrieve list of all FAQ
            const response =
                await fetch(
                    serviceURL, {
                        method: 'DELETE'
                    }
                );
            const result = await response.json();
            if (response.ok) {
                // console.log(result);
                alert("Field deleted successfully.")
                window.location = window.location;
            }
        } catch (error) {
            // Errors when calling the service; such as network error, 
            // service offline, etc
            console.log(error)
            alert('There is a problem retrieving data, please refresh the page or try again later.');
        } // error

    }
}
//#endregion