// Posting data to backend
function submitForm(formName, form) {
    // var formElements = document.forms[0].elements

    var formData = new FormData(form);
    formData.append("formName",formName)

    console.log(form)
    for (var pair of formData.entries()) {
        console.log(pair[0]+ ', ' + pair[1]); 
    }

    addDonation(formData, 'http://ec2-13-250-122-219.ap-southeast-1.compute.amazonaws.com:5003/formanswers')
}

// POST request:
async function addDonation(formdata, url) {
    // Default options are marked with *
    // console.log(data)

    return fetch(url,
        {
            method: "POST",
            body: formdata
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            alert(data.message)
            window.location.href = 'index.html'
        })
        .catch(error => {console.log(error);alert(error);})
    

    // try {
    //     const response = await fetch(url, {
    //     method: 'POST', // *GET, POST, PUT, DELETE, etc.
    //     mode: 'no-cors', // no-cors, *cors, same-origin
    //     cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    //     credentials: 'same-origin', // include, *same-origin, omit
    //     redirect: 'follow', // manual, *follow, error
    //     referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    //     body: data // body data type must match "Content-Type" header
    //     });
    //     alert(response.status)
    //     // alert(response)

    //     // return true

    //     if (response.status == 201) {
    //         alert("Item has been posted successfully")
    //         // window.location.href = "index.html"
    //         return true
    //     }
    //     console.log(response)
    //     alert(response.status)
    //     alert(response.text())
    //     return false;
    // } catch (error) {
    //     // Errors when calling the service; such as network error, 
    //     // service offline, etc
    //     // console.log(response)
    //     // console.log(error)
    //     // alert('There is a problem submitting the form, please refresh the page or try again later.');
    //     console.log(response)
    //     console.log(error)
    //     alert(error)
    //     return false
    // } // error
}
    

