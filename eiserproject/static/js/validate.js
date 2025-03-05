function validatePasswords() {
  var password = document.getElementById("password").value;
  var confirmPassword = document.getElementById("confirm-password").value;

  // Check if passwords match
  if (password !== confirmPassword) {
    alert("Passwords do not match!");
    return false;
  }

  // Password validation criteria
  var passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$/;

  if (!passwordRegex.test(password)) {
    alert(
      "Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one number, and one special character."
    );
    return false;
  }

  return true;
}
$(document).ready(function () {
  //  Toggle  Password Start
  // Initial state of the eye icons
  $("#togglePassword0").removeClass("fa-eye").addClass("fa-eye-slash");
  $("#togglePassword1").removeClass("fa-eye").addClass("fa-eye-slash");
  $("#togglePassword2").removeClass("fa-eye").addClass("fa-eye-slash");
  
  // Toggle password visibility for the current password field (profile/changepassword/)
  $("#togglePassword0").click(function() {
    const passwordInput = $("#current-password");

    // Toggle the input type and change the icon
    if (passwordInput.attr("type") === "password") {
      passwordInput.attr("type", "text");
      $(this).removeClass("fa-eye-slash").addClass("fa-eye");
    } else {
      passwordInput.attr("type", "password");
      $(this).removeClass("fa-eye").addClass("fa-eye-slash");
    }
  });


  // Toggle password visibility for the first password field
  $("#togglePassword1").click(function() {
    const passwordInput = $("#password");

    // Toggle the input type and change the icon
    if (passwordInput.attr("type") === "password") {
      passwordInput.attr("type", "text");
      $(this).removeClass("fa-eye-slash").addClass("fa-eye");
    } else {
      passwordInput.attr("type", "password");
      $(this).removeClass("fa-eye").addClass("fa-eye-slash");
    }
  });

  // Toggle password visibility for the confirm password field
  $("#togglePassword2").click(function() {
    const confirmPasswordInput = $("#confirm-password");

    // Toggle the input type and change the icon
    if (confirmPasswordInput.attr("type") === "password") {
      confirmPasswordInput.attr("type", "text");
      $(this).removeClass("fa-eye-slash").addClass("fa-eye");
    } else {
      confirmPasswordInput.attr("type", "password");
      $(this).removeClass("fa-eye").addClass("fa-eye-slash");
    }
  });
 //  Toggle  Password End
});
