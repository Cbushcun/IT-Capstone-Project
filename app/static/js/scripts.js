function validatePassword() {
    console.log("validatePassword function called"); // For debugging
    var password = document.getElementById("password");
    var verify_password = document.getElementById("verify_password");

    if (password.value !== verify_password.value) {
        console.log("Passwords do not match"); // For debugging
        alert("Passwords do not match");
        return false;
    }
    console.log("Passwords match"); // For debugging
    return true;
}