// // this is the main function called when the page is refresh
function main_function(){
    // call the check license function
    check_license()
}

function check_license(){
    fetch('/api/method/washmis_erp.templates.pages.home_page.check_licensing_status')
    .then(response => response.json())
    .then(license_data => show_hide_sign_in(license_data));
}

// function that uses the license_data to determine whether or 
// to show the sign in buttons
function show_hide_sign_in(license_data){
    // check if license is valid
    if(license_data.message.status){
        // license is active enable 
        document.getElementById("top-sign-in-button").setAttribute('href','/desk')
        document.getElementById("top-sign-in-button").innerHTML ='Sign In'
        document.getElementById("main-sign-in-link").setAttribute('href','/desk')
        document.getElementById("main-sign-in-button").innerHTML ='Sign In'
    }else{
        // license has expired disable the login button
        document.getElementById("top-sign-in-button").setAttribute('href','#licensing-section')
        document.getElementById("top-sign-in-button").innerHTML ='Renew License'
        document.getElementById("main-sign-in-link").setAttribute('href','#licensing-section')
        document.getElementById("main-sign-in-button").innerHTML ='Renew License'
    }

    // call the modify licensing section
    modify_licensing_section(license_data)
}

function modify_licensing_section(license_data){
    // check if license is valid
    if(license_data.message.status){
        // modify for checking updates
        document.getElementById("call-to-action-heading").innerHTML ='Click on the button below to check for and update system'
        document.getElementById("call-to-action-button").innerHTML ='Update'
        document.getElementById("call-to-action-button").setAttribute("onclick","updateFunction()")
        document.getElementById("call-to-action-input").setAttribute("style","display:none;")
        document.getElementById("input-field-container").setAttribute("class","col-12 col-md-4 mb-2 mb-md-0")

    }else{
        document.getElementById("call-to-action-heading").innerHTML ='Enter a valid License in the input field below'
        document.getElementById("call-to-action-button").innerHTML ='Validate'
        document.getElementById("call-to-action-button").setAttribute("onclick","validateLicense()")
        document.getElementById("call-to-action-input").setAttribute("style","")
        document.getElementById("input-field-container").setAttribute("class","col-12 col-md-9 mb-2 mb-md-0")
    }
}

function updateFunction(){
    // check if any new updates are available
    fetch('/api/method/washmis_erp.templates.pages.home_page.check_for_updates')
    .then(response => response.json())
    .then(response_json => updateSystem(response_json));
}

function updateSystem(update_status){
    if(update_status.message.status){
        // updates exists hence update system
        alert("Updating system")
    }else{
        // no new updates inform user
        alert("No new updates exists")
    }
}

// function that checks if the given license is valid
function validateLicense(){
    // check if a key is given
    var inputVal = document.getElementById("call-to-action-input").value;
    if(inputVal){
        document.getElementById("call-to-action-input").value = ""
        console.log(inputVal)
        alert("validating key")
        // now validate the given key
        fetch(`/api/method/washmis_erp.templates.pages.home_page.check_license_key_is_valid?license_key=${inputVal}`)
        .then(response => response.json())
        .then(response_json => afterLicenseValidation(response_json));
    }else{
        alert("No License key is given")
    }
}

function afterLicenseValidation(validation_status){
    // check if the license was validated
    if(validation_status.message){
        alert("Congratulation your License has been validated")
        // refresh the page
        window.refresh()
    }else{
        alert("License vaidation has failed")
    }
}

// call the main function
main_function()




