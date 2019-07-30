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
$('#post_form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!"); // sanity check
    create_post($(this));
});



// function create_post() {
//     console.log("create post is working!"); // sanity check
//     // console.log($('#id_post_content').val());
//     var value = CKEDITOR.instances['id_post_content'];
//     console.log(value.getData());
//
// }


// AJAX for posting
function create_post(this_) {
    console.log("create post is working!"); // sanity check
    var url_ = this_.attr('action');
    var title = $('#id_title');
    var postContent = CKEDITOR.instances['id_post_content'].getData();
    // var select = $('select[name="tags"]');
    // var selected = select.children("option").filter(":selected").text();
    var selected = $('select[name="tags"] :selected');
    // var author = this_.attr('author');
    // alert(selected);
    $.ajax({
        url : url_, // the endpoint
        type : "POST", // http method
        data : {
            title: title.val(),
            tags: selected.text(),
            post_content: postContent
        }, // data sent with the post request

        // handle a successful response
        success : function(json) {

            alert(json.isPinned);
            $('#id_title').val('');
            // alert( $('select[name="tags"]').html());
            //
            // $('select[name="tags"]').html('');

            // $('select[name="tags"] :selected').prop("selected", false);
            CKEDITOR.instances['id_post_content'].setData('');
            var elem = $('.post-form-collapse');
            var instance = M.Collapsible.getInstance(elem);
            instance.close(0);
            // var collection = $('//.ajax_post_display');
            // var titleBlock = collection.children('.ajax-title');
            // var tagBlock = collection.children('.ajax-tag');
            // var contentBlock = collection.children('.ajax-content');
            // var likeCommentBlock = collection.children('.ajax-like-comment');

            // likeCommentBlock.attr("id","like-" + json.postPk);
            // Changing DOM
            // titleBlock.children('h4').html(json.postTitle); //.val(json.postTitle);
            // titleBlock.children('p').children('.s8').children('.chip').html('<img src=' + json.avatarURL + '>' + json.author);
            // for (var i = 0; i < json.selectedTags.length; i++)
            // {
            //     tagBlock.append('<a class="chip">' + json.selectedTags[i] + '</a>');
            // }
            //
            // contentBlock.children('.expanded-content').html(json.postContent);
            // collection.fadeIn();

            var postDivPinned = $('.pinned-posts');
            var postDivNormal = $('.normal-posts');

            if(json.isPinned === false){
                postDivNormal.prepend(
                "<ul class='collection with-header ajax-display'>" +
                    "<li class='collection-item'>" +
                        "<h4>"+ json.postTitle +"</h4>" +
                        "<p class='row'>" +
                        "<span class='col s8 m8 l7'>" +
                            "<a href='' class='chip'>" +
                                "<img src=" + json.avatarURL +">" + json.author +
                            "</a>" +
                        "</span>" +
                        "<span class='col s4 m4 l4'>" + json.created + " ago.</span>" +
                        "</p>" +
                    "</li>" +

                    "<li class='collection-item ajax-tag'>" +
                        "Tags: " +
                    "</li>" +

                    "<li class='collection-item'>" +
                        "<div class='expanded-content'>" +
                            json.postContent +
                        "</div>" +
                    "</li>" +

                    "<li class='collection-item row' id='like-'" + json.postPk + ">" +
                        "<div class=\"col s5 m5 l5\">" +
                            "<a class='btn-flat like-btn' data-likes=" + json.likes + ">" + json.likesCountStr + "</a>" +
                        "</div>" +
                        "<a class='btn-flat comment-display-btn' href='#'>Comments</a>" +
                    "</li>" +

                    "<li class='collection-item comment-display'>" +
                        "<form method='post' action=" + json.addCommentURL + ">" +

                            "<div class='input-field col s12'>" +
                                "<textarea id='id_comment_text' class='materialize-textarea' name='comment_text' cols='40' rows='10' class='validate' ></textarea>" +
                                "<label class='' for='id_comment_text'></label>" +
                            "</div>" +
                            "<button class='btn waves-light' type='submit' name='action'>Post Comment" +
                                "<i class='material-icons right'>send</i>\n" +
                            "</button>"+
                        "</form>" +
                    "</li>" +

                "</ul>"
                );
            } else if (json.isPinned === true) {
                postDivPinned.prepend(
                "<ul class='collection with-header ajax-display'>" +
                    "<li class='collection-item'>" +
                        "<h4>"+ json.postTitle + "<a class='chip'>Pinned to Top</a> " + "</h4>" +
                        "<p class='row'>" +
                        "<span class='col s8 m8 l7'>" +
                            "<a href='' class='chip'>" +
                                "<img src=" + json.avatarURL +">" + json.author +
                            "</a>" +
                        "</span>" +
                        "<span class='col s4 m4 l4'>" + json.created + " ago.</span>" +
                        "</p>" +
                    "</li>" +

                    "<li class='collection-item ajax-tag'>" +
                        "Tags: " +
                    "</li>" +

                    "<li class='collection-item'>" +
                        "<div class='expanded-content'>" +
                            json.postContent +
                        "</div>" +
                    "</li>" +

                    "<li class='collection-item row' id='like-'" + json.postPk + ">" +
                        "<div class=\"col s5 m5 l5\">" +
                            "<a class='btn-flat like-btn' data-likes=" + json.likes + ">" + json.likesCountStr + "</a>" +
                        "</div>" +
                        "<a class='btn-flat comment-display-btn' href='#'>Comments</a>" +
                    "</li>" +

                    "<li class='collection-item comment-display'>" +
                        "<form method='post' action=" + json.addCommentURL + ">" +

                            "<div class='input-field col s12'>" +
                                "<textarea id='id_comment_text' class='materialize-textarea' name='comment_text' cols='40' rows='10' class='validate' ></textarea>" +
                                "<label class='' for='id_comment_text'></label>" +
                            "</div>" +
                            "<button class='btn waves-light' type='submit' name='action'>Post Comment" +
                                "<i class='material-icons right'>send</i>\n" +
                            "</button>"+
                        "</form>" +
                    "</li>" +

                "</ul>"
                );
            }

            var ajaxTag = $('.ajax-tag');

            for (var i = 0; i < json.selectedTags.length; i++)
            {
                ajaxTag.append('<a class="chip">' + json.selectedTags[i] + '</a>');
            }

            addToast(json.result);
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



// User Signup

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
                addToast('Password too short. Try again!');
                pass1.val('');
                pass2.val('');
            } else if(json === 'PVS'){
                addToast('Password very similar to personal information. Try again!');
                pass1.val('');
                pass2.val('');
            } else if(json === 'PTC'){
                addToast('Password too common. Try again!');
                pass1.val('');
                pass2.val('');
            } else if(json === 'PEN'){
                addToast('Password entirely numeric. Try again!');
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