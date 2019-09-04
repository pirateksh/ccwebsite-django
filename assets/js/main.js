 $(document).ready(function() {
        //Preloader
        $(window).on("load", function() {
        preloaderFadeOutTime = 500;
        function hidePreloader() {
        var preloader = $('.spinner-wrapper');
        preloader.fadeOut(preloaderFadeOutTime);
        }
        hidePreloader();
        });
        });




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
$('.post_form').on('submit', function(event){
    event.preventDefault();
    //console.log("form submitted!"); // sanity check
    create_post($(this));
});

// AJAX for posting
function create_post(this_) {
    //console.log("create post is working!"); // sanity check
    var url_ = this_.attr('action');
    var title = $('#id_title');
    var postContent = CKEDITOR.instances['id_post_content'].getData();
    postContent = $.trim(postContent);
    var selected = $('select[name="tags"] :selected');
    var successRedirectURL = this_.attr('data-success');
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

            $('#id_title').val('');
            CKEDITOR.instances['id_post_content'].setData('');
            var elem = $('.post-form-collapse');
            var instance = M.Collapsible.getInstance(elem);
            instance.close(0);

            var postDivPinned = $('.pinned-posts');
            var postDivNormal = $('.normal-posts');
            /*
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
                        "<div class='col s4 m4 l4 center'>" +
                            "<a class='btn-flat like-btn light-blue white-text' data-likes=" + json.likes + " id='like-btn-" + json.postPk + "' href='"+ json.likeURL +"'> " +
                                json.likes +
                                " <i class='material-icons'>thumb_up</i>" +
                            "</a>" +
                        "</div>" +
                        "<div class=\"col s4 m4 l4 center\">" +
                            "<a class='btn-flat comment-display-btn light-blue white-text' href='#'><i class='material-icons'>comment</i></a>" +
                        "</div>" +
                        "<form action=\"{% url 'ajax_delete_post' %}\" class=\"post-del-form\" method=\"get\" data-from=\"user_prof\" data-pk=" + json.postPk + ">" +
                        "<div class=\"col s4 m4 l4 center\">" +
                            "<a class=\"btn-flat red white-text modal-trigger\" href=\"#delete-post-modal\"><i class=\"material-icons\">delete</i></a>" +
                        "</div>" +
                        "<div id=\"delete-post-modal\" class=\"modal modal-fixed-footer\">" +
                            "<div class=\"modal-content\">" +
                                "<h4>Delete Post</h4>" +
                                "<p>Do you really want to delete this? There is no going back...</p>" +
                            "</div>" +
                            "<div class=\"modal-footer\">" +
                                "<button class=\"btn-flat post-del-btn-no green white-text\" type=\"submit\">No</button>" +
                                "<button class=\"btn-flat red white-text\" type=\"submit\">Yes</button>" +
                            "</div>" +
                        "</div>" +
                        "</form>" +
                    "</li>" +

                    "<li class='collection-item comment-display'>" +
                        "<form method='post' action='" + json.addCommentURL + "'>" +

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
                        "<div class=\"col s4 m4 l4 center\">" +
                            "<a class='btn-flat like-btn light-blue white-text' data-likes=" + json.likes + " id='like-btn-" + json.postPk + "' href='"+ json.likeURL +"'> " +
                                json.likes +
                                " <i class='material-icons'>thumb_up</i>" +
                            "</a>" +
                        "</div>" +
                        "<div class=\"col s4 m4 l4 center\">" +
                            "<a class='btn-flat comment-display-btn light-blue white-text' href='#'><i class='material-icons'>comment</i></a>" +
                        "</div>" +
                        "<form action=\"{% url 'ajax_delete_post' %}\" class=\"post-del-form\" method=\"get\" data-from=\"user_prof\" data-pk=" + json.postPk + ">" +
                        "<div class=\"col s4 m4 l4 center\">" +
                            "<a class=\"btn-flat red white-text modal-trigger\" href=\"#delete-post-modal\"><i class=\"material-icons\">delete</i></a>" +
                        "</div>" +
                        "<div id=\"delete-post-modal\" class=\"modal modal-fixed-footer\">" +
                            "<div class=\"modal-content\">" +
                                "<h4>Delete Post</h4>" +
                                "<p>Do you really want to delete this? There is no going back...</p>" +
                            "</div>" +
                            "<div class=\"modal-footer\">" +
                                "<button class=\"btn-flat post-del-btn-no green white-text\" type=\"submit\">No</button>" +
                                "<button class=\"btn-flat red white-text\" type=\"submit\">Yes</button>" +
                            "</div>" +
                        "</div>" +
                        "</form>" +
                    "</li>" +

                    "<li class='collection-item comment-display'>" +
                        "<form method='post' action='" + json.addCommentURL + "'>" +

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

            $('.no-post-yet').fadeOut();

            var ajaxTag = $('.ajax-tag');

            for (var i = 0; i < json.selectedTags.length; i++)
            {
                ajaxTag.append('<a class="chip">' + json.selectedTags[i] + '</a>');
            }
            */
            // if(json.comingFrom === "home") {
            //     location.href =
            // } else if (json.comingFrom === 'user-prof') {
            //     location.href =
            // }
            location.href = successRedirectURL;

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

//Deleting post - NO
$('.post-del-btn-no').click(function (event) {
    event.preventDefault();
    var PK = $(this).attr('data-pk');
    var elem = $('#delete-post-modal-' + PK);
    var instance = M.Modal.getInstance(elem);
    instance.close();
});

//Deleting post - YES
$('.post-del-form').submit(function (event) {
    event.preventDefault();
    // alert('delete success!');
    var this_ = $(this);
    var url = this_.attr('action');
    var comingFrom = this_.attr('data-from');
    // alert(comingFrom);
    var postPK = this_.attr('data-pk');

    $.ajax({
        url: url,
        type: "GET",
        data: {
            coming_from: comingFrom,
            post_pk: postPK
        },

        success: function (json) {

            var postDiv;

            if (json.result === "SS") {

                if (json.comingFrom === "user_prof") {

                    postDiv = $('#user-prof-post-' + json.postPK);

                } else if (json.comingFrom === "home") {

                    postDiv = $('#home-post-' + json.postPK);

                }

                postDiv.css('display', 'none');
                // postDiv.fadeOut(2000);
                addToast("Post deleted successfully!");
            } else if (json.result === "ERR") {
                addToast('Oops! We have encountered an error. Try Again!');
            }

        },

        error: function () {
            addToast('Oops! We have encountered an error. Try Again!');
        }
    });
});

// Edit post
$('.edit-btn').click(function (event) {

    var this_ = $(this);
    var postPK = this_.attr('data-pk');
    var postData = this_.attr('data-val');
    CKEDITOR.instances['id_post_content_' + postPK].setData(postData);

    $('#post-edit-form-' + postPK).submit(function (e) {
        e.preventDefault();
        var form = $(this);
        var updatedTitle = $('#id-title-' + postPK);
        var url = form.attr('action');
        var updatedTags = $('#tags-edit-' + postPK).children().filter(':selected').text();
        //alert(updatedTags);
        var updatedContent = CKEDITOR.instances['id_post_content_' + postPK].getData();
        $.ajax({
            url: url,
            type: 'POST',
            data: {
                pk: postPK,
                title: updatedTitle.val(),
                tags: updatedTags,
                post_content: updatedContent,
            },
            success: function (json) {

                if (json.result === 'SS') {
                    //(json.content + json.title + json.selectedTags);
                    var ulCollection = $('#user-prof-post-' + postPK);
                    ulCollection.children('.title').children('#post-head-m-down').html(json.title);
                    ulCollection.children('.title').children('#ost-head-s-down-l').html(json.title);
                    ulCollection.children('.title').children('#post-head-m-up').html(json.title);
                    // $('#id-title-' + json.postPK).val(json.title);
                    var tags = ulCollection.children('.tag');
                    var likeBtn = $('#like-btn-' + json.postPK);
                    likeBtn.attr('href', json.likeUrl);
                    tags.html("Tags:");

                    for (var i = 0; i < json.selectedTags.length; i++) {
                        tags.append('<a class="chip">' + json.selectedTags[i] + '</a>');
                    }

                    ulCollection.children('#p').html(json.content);
                    CKEDITOR.instances['id_post_content_' + postPK].setData(json.content);

                    var elem = $('#edit-post-modal-' + postPK);
                    var instance = M.Modal.getInstance(elem);
                    instance.close();
                    addToast('Post edited successfully!');

                } else if (json.result === 'ERR') {
                    addToast('Oops! We have encountered an error. Try Again!');
                }
            },

            error: function () {

            }
        });
    });
});

// For reply fadeToggle()
$(".comment-reply-btn").click(function (event) {
    event.preventDefault();
    $(this).parent().next(".comment-reply").fadeToggle();
});

// For comment fadeToggle()
$(".comment-display-btn").click(function (event) {
    event.preventDefault();
    $(this).parent().parent().next('.comment-display').fadeToggle();
});

// Like Feature
$('.like-btn').click(function (event) {
   event.preventDefault();
   //console.log("like btn clicked!");
   var this_ = $(this);
   var url = this_.attr('href');
   var likesCount = parseInt(this_.attr('data-likes')) || 0;

   $.ajax({
       url: url,
       method: "GET",
       data: {},
       success: function (json) {
           if(json.result !== "ERR") {

               if(json.result === "UNA") {
                   addToast("Login to like post!");
                   var elem = $('#modal1');
                   var instance = M.Modal.getInstance(elem);
                   instance.open();
               } else {
                   var btn = $('#like-btn-' + json.postPK);
                   if(json.result === "UNLIKED") {
                       //console.log("UNLIKED");
                       btn.html(
                           json.likesCount +
                           " <i class='material-icons large'>thumb_up</i>"
                        );
                        addToast("Unliked");
                   } else if (json.result === "LIKED") {
                       //console.log("LIKED");
                        btn.html(
                           json.likesCount +
                           " <i class='material-icons large'>thumb_down</i>"
                        );
                        addToast("Liked");
                   }
               }
           } else if (json.result === "ERR") {
               addToast('Oops! We have encountered an error. Try Again!');
           }
       },
       error: function (json) {
           addToast('Oops! We have encountered an error. Try Again!');
       }
   });
});

// Comment AJAX

$('.comment-add-form').submit(function (event) {
   event.preventDefault();
   //console.log("Post comment button clicked");
   var this_ = $(this);
   var commentType = this_.attr('data-type');
   var postPK = this_.attr('post-pk');
   var commentPK = this_.attr('comment-pk') || 0;
   var url = this_.attr('action');
   var commentContent;
   if(commentType === 'comment') {
       commentContent = CKEDITOR.instances['id_comment_' + postPK].getData();
   } else if(commentType === 'reply') {
       commentContent = CKEDITOR.instances['id_comment_reply_' + postPK + '_' + commentPK].getData();
   }
   commentContent = $.trim(commentContent);
   //console.log(commentContent);

   $.ajax({
       url: url,
       method: "POST",
       data: {
           post_pk: postPK,
           comment_pk: commentPK,
           comment_content: commentContent
       },
       success: function (json) {
           if(json.result === "SS") {
                //console.log("Everything good!");
                if(commentType === 'comment') {
                    var commentDiv = $('#comment-' + postPK);
                    commentDiv.prepend(
                        "<blockquote>" +
                            commentContent +
                            "<footer>" +
                                "via -" +
                                "<a class='chip' href='"+ json.userProfileURL +"'>" +
                                    "<img src=" + json.avatarURL +">" +
                                    json.userName +
                                "</a>" +
                                "| " + json.timestamp + " ago | " +
                                    json.countStr +
                                "<a class='comment-reply-btn' href='#'>Reply</a>" +
                            "</footer>" +
                            "<div class='comment-reply' id='reply-" + postPK + "-" + commentPK + "' style='display: none;'>" +
                                "<form class='comment-add-form' method='post' action="+ json.addCommentURL +" post-pk=" + postPK +" comment-pk="+ commentPK +" data-type='reply'>" +
                                    "{% csrf_token %}" +
                                    "<script type=\"text/javascript\" src=\"/static/ckeditor/ckeditor-init.js\" data-ckeditor-basepath=\"/static/ckeditor/ckeditor/\" id=\"ckeditor-init-script\"></script>\n" +
                                    "<script type=\"text/javascript\" src=\"/static/ckeditor/ckeditor/ckeditor.js\"></script>" +
                                    "<div class=\"django-ckeditor-widget\" data-field-id='id_comment_reply_" + postPK + "_" + commentPK + "' style='display: inline-block;'>" +
                                        "<textarea cols='40' id='id_comment_reply_" + postPK + "_" + commentPK + "' name='post_content' rows=\"10\" required data-processed=\"0\" data-config=\"{&quot;skin&quot;: &quot;moono-lisa&quot;, &quot;toolbar_Basic&quot;: [[&quot;Source&quot;, &quot;-&quot;, &quot;Bold&quot;, &quot;Italic&quot;]], &quot;toolbar_Full&quot;: [[&quot;Styles&quot;, &quot;Format&quot;, &quot;Bold&quot;, &quot;Italic&quot;, &quot;Underline&quot;, &quot;Strike&quot;, &quot;SpellChecker&quot;, &quot;Undo&quot;, &quot;Redo&quot;], [&quot;Link&quot;, &quot;Unlink&quot;, &quot;Anchor&quot;], [&quot;Image&quot;, &quot;Flash&quot;, &quot;Table&quot;, &quot;HorizontalRule&quot;], [&quot;TextColor&quot;, &quot;BGColor&quot;], [&quot;Smiley&quot;, &quot;SpecialChar&quot;], [&quot;Source&quot;]], &quot;toolbar&quot;: &quot;custom&quot;, &quot;height&quot;: &quot;15vh&quot;, &quot;width&quot;: false, &quot;filebrowserWindowWidth&quot;: 940, &quot;filebrowserWindowHeight&quot;: 725, &quot;resize_dir&quot;: &quot;vertical&quot;, &quot;toolbar_custom&quot;: [[&quot;Styles&quot;, &quot;Format&quot;, &quot;Bold&quot;, &quot;Italic&quot;, &quot;Underline&quot;, &quot;Strike&quot;, &quot;CodeSnippet&quot;], [&quot;Link&quot;, &quot;Unlink&quot;, &quot;Anchor&quot;], [&quot;Image&quot;, &quot;Table&quot;, &quot;HorizontalRule&quot;], [&quot;TextColor&quot;, &quot;BGColor&quot;], [&quot;Smiley&quot;, &quot;SpecialChar&quot;], [&quot;Source&quot;]], &quot;extraPlugins&quot;: &quot;resize&quot;, &quot;filebrowserUploadUrl&quot;: &quot;/ckeditor/upload/&quot;, &quot;filebrowserBrowseUrl&quot;: &quot;/ckeditor/browse/&quot;, &quot;language&quot;: &quot;en-us&quot;}\" data-external-plugin-resources=\"[]\" data-id='id_comment_reply_" + postPK + "_" + commentPK + "' data-type=\"ckeditortype\"></textarea>\n" +
                                    "</div>" +
                                    "<input type=\"hidden\" name=\"parent_id\" value=\"{{ comment.id }}\">" +
                                    "<button class=\"btn waves-light\" type=\"submit\" name=\"action\">Reply" +
                                        "<i class=\"material-icons right\">send</i>" +
                                    "</button>" +
                                "</form>" +
                            "</div>" +
                        "</blockquote>"
                    );
                    commentContent = CKEDITOR.instances['id_comment_' + postPK].setData('');
                    addToast("Comment Added Successfully!")
                } else if (commentType === 'reply') {
                    var replyDiv = $('#reply-' + postPK + '-' + commentPK);
                    replyDiv.prepend(
                        "<blockquote>" +
                            commentContent +
                            "<footer>" +
                                "via -" +
                                "<a class='chip' href='" + json.userProfileURL +"'>" +
                                    "<img src='" + json.avatarURL +"'>" +
                                    json.userName +
                                "</a>" +
                                "<span id='comment-timestamp' style='color: #0f74a8;'>" +
                                    "| " + json.timestamp + " ago |" +
                                "</span>" +
                            "</footer>" +
                        "</blockquote>" +
                        "<div class=\"divider\"></div>"
                    );
                    CKEDITOR.instances['id_comment_reply_' + postPK + '_' + commentPK].setData('');
                    addToast("Reply Added Successfully!")
                }
           } else if (json.result === "ERR") {
               addToast('Oops! We have encountered an error. Try Again!');
           }
       },
       error: function (json) {
           addToast('Oops! We have encountered an error. Try Again!');
       }
   })
});

// Preloader

// document.addEventListener("DOMContentLoaded", function(){
// 	$('.preloader-background').delay(1700).fadeOut('slow');
//
// 	$(' .preloader-wrapper')
// 		.delay(1700)
// 		.fadeOut();
// });