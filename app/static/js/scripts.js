// jQuery Scripting

// Create a new <script> element for jQuery
var jqueryScript = document.createElement('script');

// Set the src attribute to the jQuery script URL
jqueryScript.src = 'https://code.jquery.com/jquery-3.6.0.min.js';

// Append the <script> element to the HTML's <head> section
document.head.appendChild(jqueryScript);
// JavaScript code goes here

src="https://js.stripe.com/v3/"
function validatePassword() {
    console.log("DEBUG: validatePassword function called"); // For debugging
    var password = document.getElementById("password");
    var verify_password = document.getElementById("verify_password");

    var passwordPattern = /^(?=.*\d)(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z]).{8,}$/;

    if (!passwordPattern.test(password.value)) {
        console.log("DEBUG: Password does not meet the criteria"); // For debugging
        alert("Password must meet the criteria.");
        return false;
    }

    if (password.value !== verify_password.value) {
        console.log("DEBUG: Passwords do not match"); // For debugging
        alert("Passwords do not match");
        return false;
    }

    console.log("DEBUG: Password meets the criteria and passwords match"); // For debugging
    return true;
}


//jQuery code here
jqueryScript.onload = function () {
    $(document).ready(function () {
        var passwordRequirements = $('.password-requirements');
        // Show the requirements when the password input is focused
        $('#password').on('focus', function () {
            passwordRequirements.show();
        });
        $('#verify_password').on('focus', function () {
            passwordRequirements.show();
        });
        // Hide the requirements when the password input loses focus (blurred)
        $('#password').on('blur', function () {
            passwordRequirements.hide();
        });
        $('#verify_password').on('blur', function () {
            passwordRequirements.hide();
        });
    });
};

