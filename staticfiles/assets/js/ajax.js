$(document).ready(function(){
    $("#checkboxError").text("");
    $("#radioError").text("");
    $("#messageError").text("");
    
    $('#bookingForm').on('submit', function(e) {
        e.preventDefault();
        $('#checkboxError').text("");
        $('#radioError').text("");
        $('#messageError').text("");
        if (validateForm()) {
            $('#bookingBtn').prop('disabled', true).html('<span class="spinner-border text-white spinner-border-sm" role="status" aria-hidden="true"></span> Submitting...');
        
            $.ajax({
                type: 'POST',
                url: '',  
                data: $(this).serialize(),
                success: function(response) {
                    if (response.success) {

                        function showNotification() {
                            var notification = document.getElementById("notification");
                            notification.style.display = "block";
                            
                            setTimeout(function() {
                                notification.style.display = "none";
                            }, 4000); 
                        }
                        showNotification();
                    
                    } else {

                        
                        
                    }
                },
                error: function(error) {
                    
                
                },
                complete: function() {
                
                    $('#bookingBtn').prop('disabled', false).html('Submit');
                }
            });
        }
    });
        

    // AJAX for login
    $('#loginForm').on('submit', function(e) {
        e.preventDefault();

        $('#loginBtn').prop('disabled', true).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Logging in...');
    
        $.ajax({
            type: 'POST',
            url: '/user/sign-in/',  
            data: $(this).serialize(),
            success: function(response) {
                if (response.success) {
                    $('#loginBtn').prop('disabled', true).html('Logging in ✔');
                    if (response.success) {

                        function showNotification() {
                            var notification = document.getElementById("notification");
                            notification.style.display = "block";
                            
                            setTimeout(function() {
                                notification.style.display = "none";
                            }, 4000); 
                        }
                        showNotification();
                    }
                    window.location.href = '/';  
                } else {
                    // Login failure
                    $("#LoginErrorMessage").text(response.message);
                    setTimeout(() => {
                        $("#LoginErrorMessage").text("");
                    }, 4000);
                    $('#loginBtn').prop('disabled', false).html('Invalid credentials');
                }
            },
            error: function(error) {
                // Handle error
                
                
            },
            // complete: function() {
     
            //     $('#loginBtn').prop('disabled', false).html('Login');
            // }
        });
    });
    $('#ContactForm').on('submit', function(e) {
        e.preventDefault();
 
        $('#contactSubmit').prop('disabled', true).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Submitting...');
    
        $.ajax({
            type: 'POST',
            url: '/contact/', 
            data: $(this).serialize(),
            success: function(response) {
                if (response.success) {
                    function showNotification() {
                        var notification = document.getElementById("notification");
                        notification.style.display = "block";
                        
                        setTimeout(function() {
                            notification.style.display = "none";
                        }, 4000); 
                    }
                    showNotification();
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
                
             
                
            },
            complete: function() {
                
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
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    $('.mark-as-read-btn').click(function() {
        var blogId = $(this).data('blog-id');
        var csrftoken = getCookie('csrftoken');
        $('.mark-as-read-btn').prop('disabled', true).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
        $.ajax({
            type: 'POST',
            url: '/mark-blog-as-read/',
            data: {'blog_id': blogId},
            dataType: 'json',
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.success) {
                    $('.mark-as-read-btn').prop('disabled', false).html('Read ✔');
                    // Optionally, update UI to reflect the change
                } else {
                    $('.mark-as-read-btn').prop('disabled', false).html('Failed to mark');
                }
            },
            error: function(xhr, status, error) {
                
            }
        });
    });
})








function validateForm() {
    var checkboxes = document.querySelectorAll('input[type="checkbox"][name="company_needs"]');
    var radios = document.querySelectorAll('input[type="radio"][name="company_type"]');
    var checkedCheckbox = false;
    var checkedRadio = false;
    var checkboxError = document.getElementById('checkboxError');
    var radioError = document.getElementById('radioError');
    var messageError = document.getElementById('messageError');
    var messageField = document.getElementById('message');
    var submitButton = document.getElementById('bookingBtn');
    
    checkboxes.forEach(function(checkbox) {
        if (checkbox.checked) {
            checkedCheckbox = true;
        }
    });
    
    radios.forEach(function(radio) {
        if (radio.checked) {
            checkedRadio = true;
        }
    });
    if (!checkedRadio) {
        radioError.textContent = "Please select a company type.";
        return false; // Prevent form submission
    } else {
        radioError.textContent = ""; // Clear error message
    }
    
    if (!checkedCheckbox) {
        checkboxError.textContent = "Please check at least one option for company needs.";
        return false; // Prevent form submission
    } else {
        checkboxError.textContent = ""; // Clear error message
    }
    
   

    if (messageField.value.trim() === '' || messageField.value.length < 10) {
        messageError.textContent = "Please enter a message with at least 10 characters.";
        return false; // Prevent form submission
    } else {
        messageError.textContent = ""; // Clear error message
    }
    
    // Enable the submit button
    submitButton.disabled = false;
    
    return true; // Allow form submission
}












function assignPassword() {
    // Get the value of password1
    var password1Value = document.getElementById('RegisterPassword1').value;
    
    // Assign the value to password2
    document.getElementById('RegisterPassword2').value = password1Value;
  }