// Posting data to backend
function submitForm(formName) {
    var formElements = document.forms[0].elements

    var formData = new FormData();
    formData.append("formName", formName);

    for (ele in formElements) {
        var eleId = formElements[ele].id;
        var eleType = formElements[ele].type;
        // console.log("Name: " + formElements[ele].name + ", Type: " + formElements[ele].type)
        if (eleType == "radio") {
            var eleName = formElements[ele].name;
            if (!formData.has(eleName)) {
                formData.append(eleName, document.querySelector(`input[name='${eleName}']:checked`).value);
                // console.log(document.querySelector("input[name='"+eleName+"']:checked").value)
            }
        }
        else if (eleType == "checkbox") {
            // store all values as a single string, values separated by ;
            var eleName = formElements[ele].name;
            if (!formData.has(eleName)) {
                checkedBoxes = document.querySelectorAll(`input[name='${eleName}']:checked`);
                values = "";
                for ( let box of checkedBoxes) {
                    values += box.value + ";"
                }
                formData.append(eleName, values.slice(0,-1));
            }
        }
        else if (eleType == "file") {
            if (formElements[ele].files.length == 0) {
                var label = $(`label[for=${eleId}]`).text();
                alert(`Please input ${label}!`)
                return false;
            }
            formData.append(eleId, formElements[ele].files[0].name);
            formData.append("file" + eleId, formElements[ele].files[0]);
        }
        else {
            formData.append(eleId, formElements[ele].value);
        }
    }

    addDonation(formData, 'http://127.0.0.1:5003/formanswers').then(function checkRes(result){
        alert(result)
    })
}

// POST request:
async function addDonation(data, url) {
    // Default options are marked with *
    // console.log(data)

    try {
        const response = await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'no-cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: data // body data type must match "Content-Type" header
        });
        // alert(response)

        return "OK"

        // if (response.status == 201) {
        //     alert("Item has been posted successfully")
        //     window.location.href = "index.html"
        //     return true
        // }
        // alert("fk u" + response)
        // return false;
    } catch (error) {
        // Errors when calling the service; such as network error, 
        // service offline, etc
        // console.log(response)
        // console.log(error)
        // alert('There is a problem submitting the form, please refresh the page or try again later.');
        return false
    } // error
}
    

