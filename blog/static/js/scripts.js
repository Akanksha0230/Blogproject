document.addEventListener('DOMContentLoaded', function() {
    attachPaginationEventListeners();

    document.getElementById('search-form').addEventListener('submit', function(event) {
        event.preventDefault();
        loadPage(1);  // Search starts from page 1
    });
});

function attachPaginationEventListeners() {
    document.querySelectorAll('#pagination-controls a').forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            let page = this.getAttribute('data-page');
            loadPage(page);
        });
    });
}

function loadPage(page) {
    let form = document.getElementById('search-form');
    let formData = new FormData(form);
    formData.append('page', page);

    let xhr = new XMLHttpRequest();
    xhr.open('GET', '?' + new URLSearchParams(formData).toString(), true);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let response = xhr.responseText;
            let parser = new DOMParser();
            let doc = parser.parseFromString(response, 'text/html');
            let newBlogList = doc.querySelector('#blog-list').innerHTML;
            let newPaginationControls = doc.querySelector('#pagination-controls').innerHTML;
            document.querySelector('#blog-list').innerHTML = newBlogList;
            document.querySelector('#pagination-controls').innerHTML = newPaginationControls;

            // Reattach event listeners
            attachPaginationEventListeners();
        }
    };
    xhr.send();
}

function getCSRFToken() {
    return $('input[name=csrfmiddlewaretoken]').val();
}

$(document).ready(function () {
      // Login form submission
      $('#login-btn').click(function(event) {
        event.preventDefault(); 
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
        console.log($('#create-blog-form').serialize());
        // Get the CSRF token from the cookie
        var csrftoken = $('input[name=csrfmiddlewaretoken]').val();

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
                    location.reload(); 
                    alert("Blog created successfully!!!") // Refresh the page on success
                } else {
                    alert('An error occurred: ' + JSON.stringify(response.errors));
                }
            },
            error: function() {
                alert('An error occurred while creating the blog.');
            }
        });
    });

    $('#updateBlogForm').submit(function(event) {
        event.preventDefault();
        console.log("Form submission intercepted.");
         // Get the CSRF token from the form
        var csrftoken = $('input[name=csrfmiddlewaretoken]').val();
    
        // Get the form data
        var formData = new FormData(this);
        formData.append('csrfmiddlewaretoken', csrftoken);
    
            // Send the AJAX request
            $.ajax({
                type: 'POST',
                url: '/blog/update/',  // Make sure this URL matches your update URL pattern
                data: formData,
                processData: false,
                contentType: false,
                success: function(response) {
                    if (response.success) {
                        location.reload();
                        alert("Blog updated successfully!!!");
                    } else {
                        console.log("An error occurred: ", response.errors);
                        alert('An error occurred: ' + JSON.stringify(response.errors));
                    }
                },
                error: function() {
                    console.log("An error occurred while updating the blog.");
                    alert('An error occurred while updating the blog.');
                }
            });
        
    });
    $('#deleteBlogForm').submit(function(event) {
        event.preventDefault();
        
        // Get the CSRF token from the form
        var csrftoken = $('input[name=csrfmiddlewaretoken]').val();
        
        // Get the form data
        var formData = new FormData(this);
        formData.append('csrfmiddlewaretoken', csrftoken);
        
        // Send the AJAX request
        $.ajax({
            type: 'POST',
            url: '/blog/delete/',  // Make sure this URL matches your delete URL pattern
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.success) {
                    location.reload();
                    alert("Blog deleted successfully!!!");
                } else {
                    alert('An error occurred: ' + response.error);
                }
            },
            error: function() {
                alert('An error occurred while deleting the blog.');
            }
        });
    });

    $('#email-input-form').submit(function(event) {
        event.preventDefault();
        
        var email = $('#id_reset_email').val();
        var csrftoken = getCSRFToken();
        $.ajax({
            type: 'POST',
            url: '/send-otp/',
            data: {
                email: email,
                csrfmiddlewaretoken: csrftoken
            },
            success: function(response) {
                if (response.success) {
                    $('#email-input-modal').modal('hide');
                    $('#otp_email').val(email);
                    $('#otp-input-modal').modal('show');
                } else {
                    alert(response.message);
                }
            },
            error: function() {
                alert('An error occurred while sending OTP.');
            }
        });
    });
    
    // Verify OTP
    $('#otp-input-form').submit(function(event) {
        event.preventDefault();
        
        var otp = $('#otp').val();
        var email = $('#otp_email').val();
        var csrftoken = getCSRFToken();
        $.ajax({
            type: 'POST',
            url: '/verify-otp/',
            data: {
                otp: otp,
                email: email,
                csrfmiddlewaretoken: csrftoken
            },
            success: function(response) {
                if (response.success) {
                    alert('Email verification successful!');
                    $('#otp-input-modal').modal('hide');
                    $('#reset_email').val(email);  // Set the email for password reset
                    $('#new-password-modal').modal('show');
                } else {
                    alert(response.message);
                }
            },
            error: function() {
                alert('An error occurred while verifying OTP.');
            }
        });
    });
    // Set New Password
    $('#new-password-form').submit(function(event) {
        event.preventDefault();
        
        var new_password = $('#id_new_password').val();
        var confirm_password = $('#id_confirm_password').val();
        var email = $('#reset_email').val();
        var csrftoken = getCSRFToken();
        if (new_password !== confirm_password) {
            alert('Passwords do not match!');
            return;
        }

        $.ajax({
            type: 'POST',
            url: '/reset-password/',
            data: {
                email: email,
                new_password: new_password,
                confirm_password: confirm_password,
                csrfmiddlewaretoken: csrftoken
            },
            success: function(response) {
                if (response.success) {
                    alert('Password reset successful!');
                    $('#new-password-modal').modal('hide');
                } else {
                    alert(response.message);
                }
            },
            error: function() {
                alert('An error occurred while resetting the password.');
            }
        });
    });
    $("#like-btn").click(function(event) {
        event.preventDefault();
        if (window.isAuthenticated === "false") {
            alert("You need to log in to like.");
            return;
        }
        var blogId = window.blogId;
        var csrfToken = window.csrfToken;
        $.ajax({
          type: "POST",
          url: "/like/" + blogId + "/",
          data: {
            csrfmiddlewaretoken: csrfToken
          },
          success: function(response) {
            if (response.success) {
              $("#like-count").text(response.likes);
              $("#like-btn").prop("disabled", true).text("Liked");
            } else {
              alert(response.message);
            }
          },
          error: function() {
            alert("An error occurred while liking the blog.");
          }
        });
      });

      $("#comment-form").submit(function(event) {
        event.preventDefault();
        if (window.isAuthenticated === "false") {
            alert("You need to log in to add a comment.");
            return;
        }
        var content = $("#comment-content").val();
        var csrfToken = $("input[name='csrfmiddlewaretoken']").val();
        var blogId = window.blogId;
        
        $.ajax({
            type: "POST",
            url: "/blog/" + blogId + "/comment/",
            data: {
                content: content,
                csrfmiddlewaretoken: csrfToken
            },
            success: function(response) {
                if (response.success) {
                    $("#comment-list").append(
                        '<li class="list-group-item">' + response.comment.content + ' - <strong>' + response.comment.user + '</strong> on ' + response.comment.date + '</li>'
                    );
                    $("#comment-content").val('');
                } else {
                    alert(response.message);
                }
            },
            error: function(xhr, status, error) {
                alert("An error occurred while adding the comment.");
                console.error(xhr.responseText);
            }
        });
    });
    $('[data-load-blog-list="true"]').on('click', function(event) {
        event.preventDefault();
        
        $.ajax({
            url: '/profile/',  // Ensure this URL matches the URL pattern for the profile view
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                var blogTitles = data.blog_titles;
                var blogList = $('#user-blog-list');
                blogList.empty();
                if (blogTitles.length > 0) {
                    $.each(blogTitles, function(index, blog) {
                        var blogUrl = '/blog/' + blog.id + '/';  // Constructing the URL dynamically
                        blogList.append('<li><h5><a href="' + blogUrl + '">' + blog.title + '</a></h5> - <strong>' + blog.date + '</strong></li>');
                    });
                } else {
                    blogList.append('<li>No blog posts found.</li>');
                }
            },
            error: function(xhr, status, error) {
                console.error('An error occurred while fetching blog posts:', error);
                $('#user-blog-list').append('<li>An error occurred while loading blog posts.</li>');
            }
        });
    });  
});
