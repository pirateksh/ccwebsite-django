$(function() {

    // This function gets cookie with a given name
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
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url === origin || url.slice(0, origin.length + 1) === origin + '/') ||
            (url === sr_origin || url.slice(0, sr_origin.length + 1) === sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});



// Submit post on submit
// $('#').on('submit', function(event){
//     event.preventDefault();
//     console.log("form submitted!"); // sanity check
//     create_post();
// });



// function create_post() {
//     console.log("create post is working!"); // sanity check
//     console.log($('#id_post_content').val());
// }


// AJAX for posting
// function create_post() {
//     console.log("create post is working!") // sanity check
//     $.ajax({
//         url : "create_post/", // the endpoint
//         type : "POST", // http method
//         data : { the_post : $('#post-text').val() }, // data sent with the post request
//
//         // handle a successful response
//         success : function(json) {
//             $('#post-text').val(''); // remove the value from the input
//             console.log(json); // log the returned json to the console
//             console.log("success"); // another sanity check
//         },
//
//         // handle a non-successful response
//         error : function(xhr,errmsg,err) {
//             $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
//                 " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
//             console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
//         }
//     });
// };



// Submit post on submit
$('#signup_form').on('submit', function(event){
    event.preventDefault();
    var successRedirectURL = $(this).attr('data-success');
    // console.log("form submitted!"); // sanity check
    create_user(successRedirectURL);
});

// AJAX for signup
function create_user(successRedirectURL) {
    // console.log("create user is working!"); // sanity check
    var url = $('#signup_form').attr('action');
    var username = $('#id_username');
    var f_name = $('#id_first_name');
    var l_name = $('#id_last_name');
    var email = $('#id_email');
    var choice = $('.st_choice:checked');
    var pass1 = $('#id_password1');
    var pass2 = $('#id_password2');

    $.ajax({
        url : url, // the endpoint
        type : "POST", // http method
        data : {
            username: username.val(),
            first_name: f_name.val(),
            last_name: l_name.val(),
            email: email.val(),
            choice: choice.val(),
            password1: pass1.val(),
            password2: pass2.val()
        }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#post-text').val(''); // remove the value from the input
            if (json === 'UAR'){
                addToast('Username already registered. Try again!');
                username.val('');
                pass1.val('');
                pass2.val('');
                // alert('User with that username already registered.');
            } else if (json === 'EAR') {
                addToast('Email already registered. Try again!');
                email.val('');
                pass1.val('');
                pass2.val('');
                // alert('User with that Email already registered.');
            } else if (json === 'PNM'){
                addToast("Passwords didn't match. Try again!");
                pass1.val('');
                pass2.val('');
            } else if(json === 'PTS'){
                addToast('Password too short. Try again!')
                pass1.val('');
                pass2.val('');
            } else if(json === 'PVS'){
                addToast('Password very similar to personal information. Try again!')
                pass1.val('');
                pass2.val('');
            } else if(json === 'PTC'){
                addToast('Password too common. Try again!')
                pass1.val('');
                pass2.val('');
            } else if(json === 'PEN'){
                addToast('Password entirely numeric. Try again!')
                pass1.val('');
                pass2.val('');
            } else if (json === 'ERR'){
                addToast('Oops! We have encountered an error. Try Again!');
                pass1.val('');
                pass2.val('');
            }
            else if (json === 'SS'){
                location.href = successRedirectURL;
                addToast('Signup Successful!');
            }

            // console.log('This comes from JSON:'+json); // log the returned json to the console
            // console.log("success"); // another sanity check
            //
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            // $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
            //     " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            // console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            addToast('Oops! We have encountered an error. Try Again!');
        }
    });
}


// AJAX for Login

$('#login_form').on('submit', function(event){
    event.preventDefault();
    // console.log("form submitted!"); // sanity check
    login_user($(this));
});

function login_user(this_) {
    var successRedirectURL = this_.attr('data-success');
    var url = this_.attr('action');
    var username = $('#login_username').val();
    var password = $('#login_password').val();

    $.ajax({
        url: url,
        type: "POST",
        data: {
            username: username,
            password: password
        },

        success: function (data) {
            if(data === 'LS') {
                location.href = successRedirectURL;
                addToast('Login Success!')
            } else if (data === 'LF') {
                $('#login_username').val('');
                $('#login_password').val('');
                addToast('Login failed. Try again!');
            } else {
                addToast('Oops! We have encountered an error. Try Again!');
            }
        },

        error: function (data) {
            addToast('Oops! We have encountered an error. Try Again!');
        }
    });
}