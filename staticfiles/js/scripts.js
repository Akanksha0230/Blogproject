import Cookies from 'js-cookie';

// Now you can use Cookies object to set, get, and delete cookies
Cookies.set('name', 'value');

$(document).ready(function () {
    function getCSRFToken() {
        return $("input[name='csrfmiddlewaretoken']").val();
    }

      // Login form submission
      $('#login-btn').click(function(event) {
        event.preventDefault();
        console.log('Login button clicked');  
        var formData = $('#login-form').serialize();
        
        $.ajax({
            type: 'POST',
            url: '/login/',
            data: formData,
            success: function(response) {
                if (response.success) {
                    location.reload();  // Refresh the page or redirect as needed
                } else {
                    alert('Please enter correct username and password.');
                }
            },
            error: function(response) {
                alert('An error occurred while fun login .');
            }

         });
       });

    // Logout form submission
    $(document).ready(function() {
        $('#logout-btn').click(function(event) {
            event.preventDefault();
    
            var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
            
            // Log the CSRF token to check its correctness
            console.log(csrfToken);
    
            $.ajax({
                type: 'POST',
                url: '/logout/',
                data: {
                    csrfmiddlewaretoken: csrfToken
                },
                success: function(response) {
                    if (response.success) {
                        location.reload();  // Refresh the page or redirect as needed
                    } else {
                        alert('An error occurred while logging out.');
                    }
                },
                error: function() {
                    alert('An error occurred while logging out.');
                }
            });
        });
    });
});

    $('#signup-btn').click(function () {
        var formData = new FormData($('#signup-form')[0]);
        $.ajax({
            type: 'POST',
            url: '/register/',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response.success) {
                    $('#signup-modal').modal('hide');
                    location.reload();  // Refresh the page or redirect as needed
                } else {
                    var errors = response.errors.join('<br>');
                    alert(errors);
                }
            },
            error: function () {
                alert("Signup failed. Please check the entered details.");
            }
        });
    });

    $('#create-blog-btn').click(function(event) {
        event.preventDefault();

        // Get the CSRF token from the cookie
        var csrftoken = Cookies.get('csrftoken');

        // Get the form data
        var formData = new FormData($('#create-blog-form')[0]);

        // Append the CSRF token to the form data
        formData.append('csrfmiddlewaretoken', csrftoken);

        // Send the AJAX request
        $.ajax({
            type: 'POST',
            url: '/blog/create/',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.success) {
                    location.reload();  // Refresh the page on success
                } else {
                    alert('An error occurred: ' + JSON.stringify(response.errors));
                }
            },
            error: function() {
                alert('An error occurred while creating the blog.');
            }
        });
    });

    $('#password-reset-btn').click(function () {
        var email = $('#id_reset_email').val();
        $.ajax({
            type: 'POST',
            url: '{% url "password_reset" %}',
            data: {
                csrfmiddlewaretoken: getCSRFToken(),
                email: email
            },
            success: function (response) {
                alert("Password reset email sent.");
            },
            error: function (xhr) {
                alert("Failed to send password reset email.");
            }
        });
    });

