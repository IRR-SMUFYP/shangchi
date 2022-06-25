// get column headers
$(document).ready(function() {
    $('#example').DataTable( {
        ajax: {
            url: 'sth',
            dataSrc: 'data',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            type: "GET",
            dataType: "json"
        },
        columns: [ 
            { data: 'sth' }
        ],
        fixedHeader: true,
    });

} );    

function editSpecificRow(form) {
    if (document.getElementById("save-btn") == null) {
        document.getElementById("edit-section").innerHTML += "<br>" + 
                                                            "<button type='button' id='save-btn' class='btn btn-outline-secondary' onclick='edit" + form + "()'>Save Changes</button>" 
    }
    $("#edit-section").show();
    $("#del-section").hide();
    if (form == "Inventory") {
        document.querySelector('[placeholder="donationID"]').setAttribute("onchange", "fillDonationDetails(this.value)");
        document.getElementById("edit-photo").style.display = "none";
        $("#donation").hide();
    }
    else if (form == "Wishlist") {
        document.querySelector('[placeholder="wishlistID"]').setAttribute("onchange", "fillWishlistDetails(this.value)");
        $("#wishlist").hide();
    }
    else if (form == "Request") {
        document.querySelector('[placeholder="reqID"]').setAttribute("onchange", "fillRequestDetails(this.value)");
        $("#request").hide();
    }
    else if (form == "SuccessfulMatches") {
        document.querySelector('[placeholder="matchID"]').setAttribute("onchange", "fillSuccessfulMatchesDetails(this.value)");
        $("#successfulMatch").hide();
    }
    else if (form == "Accounts") {
        document.querySelector('[placeholder="username"]').setAttribute("onchange", "fillUserDetails(this.value)");
        $("#account").hide();
    }
    else if (form == "DeliveryRequest") {
        $("#deliveryRequest").hide();
        document.querySelector('[placeholder="matchID"]').setAttribute("onchange", "fillDeliveryRequestDetails(this.value)");
    }
}

function getEditDetails(fields) {
    columnDetails = fields["columnDetails"];
    fieldArr = []
    for (field in fields) {
        fieldObj = {}
        for (fieldID in columnDetails) {
            if (columnDetails[fieldID] == field) {
                fieldObj["fieldID"] = fieldID;
                fieldObj["fieldName"] = field;
                fieldObj["fieldType"] = typeof(fields[field])
                fieldObj["placeholder"] = field;
                fieldObj["formName"] = "edit-section";
            }
        }
        if (field == "reqID") {
            fieldArr.unshift(fieldObj);
        }
        else if (["donationID", "wishlistID", "matchID", "username"].includes(field)) {
            fieldArr.unshift(fieldObj);
        }
        else if (field != "timeSubmitted") {
            if (field != "matchDate" && field != "Item Photo" && field != "itemName") {
                fieldArr.push(fieldObj);
            }
        }
    }
    for (i = 0; i < fieldArr.length - 1; i++) {
        fieldInput = fieldArr[i];
        if (fieldInput.fieldType == "string") {
            buildText(fieldInput);
        }
        else if (fieldInput.fieldType == "number") {
            buildNumber(fieldInput);
        }
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

async function retrieveFormAdmin(formName) {
    document.getElementById("edit-section").style.display = "none";
    document.getElementById("del-section").style.display = "none";
    if (formName == "request") {
        $("#request").show();
    }
    else if (formName == "successfulMatch") {
        $("#successfulMatch").show();
    }
    else if (formName == "account") {
        $("#account").show();
    }
    else if (formName == "deliveryRequest") {
        $("#deliveryRequest").show();
    }
    else if (formName == "donation" || formName == "wishlist") {
        var serviceURL = "http://127.0.0.1:5003/formbuilder/" + formName;
        if (formName == "donation") {
            document.getElementById("edit-photo").style.display = "none";
            document.getElementById("donation").style.display = "block";
        }
        else if (formName == "wishlist") {
            document.getElementById("wishlist").style.display = "block";
        }
    
        if (document.getElementById(formName).innerHTML == "") {
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
        
                    var contactField = `<div id="contactField" class="col-md-6">
                                            <label for="contactNo" class="form-label">Contact Number</label>
                                            <input required type="number" class="form-control" id="contactNo" value="undefined" name="contactNo">
                                        </div>`
                    var itemNameField = `<!--On change of this dropdown, auto get item names listed under this category-->
                                        <div class="col-6">
                                            <label for="itemCategoryOptions" class="form-label">Item Category</label>
                                            <select onchange="populateSubCat(this)" class="form-select" id="itemCategoryOptions" name="category"
                                                required>
                                                <!--Dynamically dropdown categories listed in existing db-->
                                            </select>
                                        </div>`
                    var subCatField = `<div class="col-6">
                                            <label for="subCatOptions" class="form-label">Sub-Category</label>
                                            <select onchange="populateItemNames(this)" class="form-select" id="subCatOptions" name="subcat"
                                                required>
                                                <!--Dynamically dropdown subcats listed in existing db-->
                                            </select>
                                        </div>`
                    var catField = `<!--Option value for item name needs to be dynamic, based on category-->
                                        <div class="col-6">
                                            <label for="itemNameOptions" class="form-label">Item Name</label>
                                            <select class="form-select" id="itemNameOptions" name="itemName" required>
                                                <!--Dynamically update item names-->
                                            </select>
                                        </div>`;
                    var addButton = `<br><button id="submitBtn" type="button" onclick="submitForm('${formName}', form)" class="btn btn-outline-secondary col-2">Submit</button>`
                    
                    document.getElementById(formName).innerHTML += contactField + itemNameField + subCatField + catField + addButton;
        
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
                }
            } catch (error) {
                // Errors when calling the service; such as network error, 
                // service offline, etc
                console.log(error)
                alert('There is a problem retrieving data, please refresh the page or try again later.');
            } // error
        }
    }
}

function addRow(formName) {
    reqFormElements = document.forms[0].elements;
    // console.log(reqFormElements);
    var formData = new FormData();
    for (ele in reqFormElements) {
        // console.log(reqFormElements[ele])
        console.log(reqFormElements[ele].id);
        if ((["donationID", "migrantID", "postalCode","donorID", "reqID", "matchID", "driverID"]).includes(reqFormElements[ele].id)) {
            if (reqFormElements[ele].value == "") {
                alert("Please do not leave any blanks.");
                return "error";
            }
        }
        eleName = reqFormElements[ele].name;
        eleVal = reqFormElements[ele].value;
        console.log(eleName, eleVal);
        formData.append(eleName, eleVal);
    }
    console.log(formData);
    if (formName == "request") {
        var serviceURL = "http://127.0.0.1:5003/request";
    }
    else if (formName == "successfulMatch") {
        var serviceURL = "http://127.0.0.1:5003/addMatch";
    }
    else if (formName == "account") {
        var serviceURL = "http://127.0.0.1:5003/addUser"
    }
    else if (formName == "deliveryRequest") {
        var serviceURL = "http://127.0.0.1:5003/addDeliveryRequest"
    }
    $(async () => {
        try {
            const response =
            await fetch(
                serviceURL, { 
                    method: 'POST', // *GET, POST, PUT, DELETE, etc.
                    mode: 'cors', // no-cors, *cors, same-origin
                    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
                    credentials: 'same-origin', // include, *same-origin, omit
                    redirect: 'follow', // manual, *follow, error
                    referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
                    body: formData // body data type must match "Content-Type" header
                });
            const result = await response.json();
            alert("Row successfully added!")
            window.location.reload()
        }
        catch (error) {
            // Errors when calling the service; such as network error, 
            // service offline, etc
            alert('There is a problem adding the data, please try again later.');
        } // error
    });
}

function deleteRow(formName) {
    document.getElementById(formName).style.display = "none";
    document.getElementById("del-section").style.display = "block";
    if (formName == "donation") {
        id = "donationID"
    }
    else if (formName == "wishlist") {
        id = "wishlistID"
    }
    else if (formName == "request") {
        id = "reqID"
    }
    else if (formName == "successfulMatch") {
        id = "matchID"
    }
    else if (formName == "account") {
        id = "username"
    }
    else if (formName == "deliveryRequest") {
        id = "matchID (delivery)"
    }
    document.getElementById("del-section").innerHTML = `<div class='col-md-6'>
                                                            <label for="${id}" class="form-label">${id}</label>
                                                            <input required type="text" class="form-control" id="${id}" placeholder="${id}"> 
                                                            <br>
                                                            <button type='button' id='del-btn' class='btn btn-outline-secondary' onclick='confirmDeleteRow("${id}")'>Delete Row</button>
                                                        </div>`;
    document.getElementById("edit-section").style.display = "none";
    document.getElementById("edit-photo").style.display = "none";
}

function confirmDeleteRow(id) {
    $(async () => {
        val = document.getElementById(id).value
        if (val == "") {
            alert("Please enter a valid input.");
            return "blank ID";
        }
        if (id == "wishlistID") {
            formName = "wishlist";
        }
        else if (id == "donationID") {
            formName = "donation";
        }
        if (id == "reqID") {
            var serviceURL = "http://127.0.0.1:5003/deleteRequest/" + val;
        }
        else if (id == "matchID") {
            var serviceURL = "http://127.0.0.1:5003/deleteMatch/" + val;
        }
        else if (id == "matchID (delivery)") {
            var serviceURL = "http://127.0.0.1:5003/deleteDeliveryRequest/" + val;
        }
        else if (id == "username") {
            var serviceURL = "http://127.0.0.1:5003/deleteUser/" + val;
        }
        else {
            var serviceURL = "http://127.0.0.1:5003/deleteRow/" + formName + "/" + val;
        }
        try {
            const response =
            await fetch(
                serviceURL, { 
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json'},
            });
            const result = await response.json();
            if (response.status == 200) {
                // success case
                alert("The data has been deleted successfully.")
                window.location.reload();
            }
            else if (response.status == 404) {
                alert('There is no such row in the database, please enter a valid ID.')
            }
            else {
                alert(`There is a problem deleting the data. Please ensure that the item you are deleting is not tagged to any requests, matches and delivery data. If it is, please delete those data in the respective tables first.`);
            }
        }
        catch (error) {
            // Errors when calling the service; such as network error, 
            // service offline, etc
            alert('There is a problem deleting the data, please try again later.');
        } // error
    });

}

function deliveryButtons(action, id) {
    document.getElementById(id).innerHTML = "";
    document.getElementById(id).style.display = "none";
    if (action == "accept") {
        document.getElementById(id).innerHTML = '<div class="row">' + 
                                                    '<div class="col-6">' + 
                                                        '<label for="matchID">matchID</label>' +
                                                        '<input class="form-control mb-2" type="text" placeholder="matchID" id="matchID">' + 
                                                    '</div>' +
                                                '</div>' +
                                                '<div class="row">' +
                                                    '<div class="col-6">' +
                                                        '<button type="button" id="acceptDelivery" class="btn btn-outline-secondary col-md-3" onclick="acceptDelivery()">Accept</button>' +
                                                    '</div>' +
                                                '</div>';
        document.getElementById(id).style.display = "";
    }
    else if (action == "update") {
        document.getElementById(id).innerHTML = '<div class="row">' + 
                                                    '<div class="col-6">' + 
                                                        '<label for="matchID">matchID</label>' +
                                                        '<input class="form-control mb-2" type="text" placeholder="matchID" id="matchID">' + 
                                                    '</div>' +
                                                    '<div class="col-6">' + 
                                                        '<label for="status">status</label>' +
                                                        '<select required class="form-select" id="status" name="status">' + 
                                                            '<option value="Assigned">Assigned</option>' +
                                                            '<option value="Out for Delivery">Out for Delivery</option>' +
                                                            '<option value="Delivered">Delivered</option>' +
                                                        '</select>' +
                                                    '</div>' +
                                                '</div>' +
                                                '<div class="row">' +
                                                    '<div class="col-6">' +
                                                        '<button type="button" id="updateDelivery" class="btn btn-outline-secondary col-md-3" onclick="updateDelivery()">Update</button>' +
                                                    '</div>' +
                                                '</div>';    
        document.getElementById(id).style.display = "";
    }
}

function acceptDelivery() {
    $(async () => {
        var driver = JSON.parse(sessionStorage.getItem("user"))
        var driverNo = driver.username;
        matchID = document.getElementById("matchID").value
        console.log(matchID);
        serviceURL = "http://127.0.0.1:5003/acceptDelivery/" + matchID;
        if (matchID == "") {
            alert("Please enter a valid input.");
            return "blank ID";
        }
        else {
            console.log(driverNo);
            data = {"driverID": driverNo}
            try {
                const response =
                await fetch(
                    serviceURL, { 
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                const result = await response.json();
                if (response.status == 200) {
                    // success case
                    alert("The delivery has been accepted successfully.")
                    window.location.reload();
                }
                else if (response.status == 404) {
                    alert("There is no such row in the database, please enter a valid ID.")
                }
                else {
                    alert("There is a problem accepting the delivery. Please try again later.");
                }
            }
            catch (error) {
                // Errors when calling the service; such as network error, 
                // service offline, etc
                alert('There is a problem accepting the delivery, please try again later.');
            } // error    
    
        }
    });
    
}

function updateDelivery() {
    $(async () => {
        matchID = document.getElementById("matchID").value;
        serviceURL = "http://127.0.0.1:5003/updateDeliveryStatus/" + matchID;
        if (matchID == "") {
            alert("Please enter a valid input.");
            return "blank ID";
        }
        else {
            deliveryStatus = document.getElementById("status").value;
            data = {"status": deliveryStatus};
            try {
                const response =
                await fetch(
                    serviceURL, { 
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                const result = await response.json();
                if (response.status == 200) {
                    // success case
                    alert("The data has been updated successfully.")
                    window.location.reload();
                }
                else if (response.status == 404) {
                    alert('There is no such row in the database, please enter a valid ID.')
                }
                else {
                    alert(`There is a problem updating the data. Please ensure that the item you are deleting is not tagged to any requests, matches and delivery data. If it is, please delete those data in the respective tables first.`);
                }
            }
            catch (error) {
                // Errors when calling the service; such as network error, 
                // service offline, etc
                alert('There is a problem updating the data, please try again later.');
            } // error    
    
        }
    });
    
}