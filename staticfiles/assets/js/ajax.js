$(document).ready(function(){
    $('#registerForm').on('submit', function(e) {
        e.preventDefault();
        
        // Disable the button and show loading state
        $('#registerBtn').prop('disabled', true).html('<span class="spinner-border text-white spinner-border-sm" role="status" aria-hidden="true"></span> Registering...');
    
        $.ajax({
            type: 'POST',
            url: '/user/sign-up/',  // Update with your register view URL
            data: $(this).serialize(),
            success: function(response) {
                if (response.success) {
                    // Registration success
                    window.location.href = '/';
                    // You may want to redirect or update the page content here
                } else {
                    // Registration failure
                    
                    const errorObj = JSON.parse(response.errors);
                

                    const message = (errorObj.username && errorObj.username[0].message) || (errorObj.email && errorObj.email[0].message);

                    $("#SignUpErrorMessage").html(`<span class="text-danger" id="LoginErrorMessage"> ${message}</span>`);
                    setTimeout(() => {
                        $("#SignUpErrorMessage").text("");
                    }, 5000);
                }
            },
            error: function(error) {
                // Handle error
                
                // Clear the error message
               
            },
            complete: function() {
                // Re-enable the button and restore its original text
                $('#registerBtn').prop('disabled', false).html('Register');
            }
        });
    });
    

    // AJAX for login
    $('#loginForm').on('submit', function(e) {
        e.preventDefault();
        
        // Disable the button and show loading state
        $('#loginBtn').prop('disabled', true).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Logging in...');
    
        $.ajax({
            type: 'POST',
            url: '/user/sign-in/',  // Update with your login view URL
            data: $(this).serialize(),
            success: function(response) {
                if (response.success) {
                    // Login success
                    
                    // Redirect to the user profile page
                    window.location.href = '/';  // Update with the actual URL
                } else {
                    // Login failure
                    $("#LoginErrorMessage").text(response.message);
                    setTimeout(() => {
                        $("#LoginErrorMessage").text("");
                    }, 4000);
                }
            },
            error: function(error) {
                // Handle error
                console.log(error.responseText);
                
            },
            complete: function() {
                // Re-enable the button and restore its original text
                $('#loginBtn').prop('disabled', false).html('Login');
            }
        });
    });
    $('#ContactForm').on('submit', function(e) {
        e.preventDefault();
        
        // Disable the button and show loading state
        $('#contactSubmit').prop('disabled', true).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Submitting...');
    
        $.ajax({
            type: 'POST',
            url: '/contact/', 
            data: $(this).serialize(),
            success: function(response) {
                if (response.success) {
                    $("#ContactErrorMessage").text('Your message has been successfully received');
                    setTimeout(() => {
                        $("#ContactErrorMessage").text("");
                    }, 5000);
                } else {
                    // Submit failure
                    const errorObj = JSON.parse(response.errors);
                

                    const message = errorObj.message[0].message;
                    
                    $("#ContactErrorMessage").text(`${message} `+'in the message field');
                    setTimeout(() => {
                        $("#ContactErrorMessage").text("");
                    }, 4000);
                }
            },
            error: function(error) {
                // Handle error
                console.log(error.errors);
                
            },
            complete: function() {
                // Re-enable the button and restore its original text
                $('#contactSubmit').prop('disabled', false).html('Submit');
            }
        });
    });
    $('#reviewForm').submit(function(e){
        e.preventDefault();
    
        $('#reviewSubmit').prop('disabled', true).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Submitting...');
    
        $.ajax({
            data: $(this).serialize(),
    
            method: $(this).attr("method"),
            url: $(this).attr("action"),
            dataType: "json",
            success: function(res){
                if (res.bool == true){
                    $("#review-res").html("Review added successfully")
                    $(".hide-comment-form").hide()
                    $(".add-review").hide()
    
                    let _html ='<div class="swiper-slide testimonial-item">'
                        _html +='<div class="testimonial-item-body">'
                        _html +='<img class="animation-slide-right bg-shape" src="static/assets/imgs/bg-shape-3.svg" alt="Shape"/>'
                        _html +='<h1>'+res.context.title+'</h1>'
                        _html +='<p>'+res.context.review+'</p>'
                        _html += '<div class="author-box d-flex align-items-center">'
                        _html +='<img src="static/assets/imgs/testimonial-1.jpg" alt="Testimonial"/>'
    
                        _html +='<div class="author-box-content">'
                        _html +='<h4>'+res.context.user+'</h4>'
                        _html +='<p>'+res.context.occupation+'</p>'
                        _html += '</div>'
                        _html += '</div>'
                        _html += '</div>'
    
                        _html += '</div>'
    
                    
                        $(".swiper-wrapper").prepend(_html)
                }
                
            },
            complete: function() {
                // Re-enable the button and restore its original text
                $('#reviewSubmit').prop('disabled', false).html('Submit');
            }
        })
    })
})



















function assignPassword() {
    // Get the value of password1
    var password1Value = document.getElementById('RegisterPassword1').value;
    
    // Assign the value to password2
    document.getElementById('RegisterPassword2').value = password1Value;
  }