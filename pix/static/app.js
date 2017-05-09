// API interaction:
function create_user() {
    var username = $('form #username').text();
    var email = $('form #email').text();
    var password = $('form #password').text();
    $.ajax({
        type: 'POST',
        url: '/users/',
        data: { username: username,
                email: email,
                password: password },
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(result) {
            // TODO load some page
            console.log(result);
        }
    });
}

function get_users() {
    $.ajax({
        type: 'GET',
        url: '/users/',
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(result){
            console.log(result);
            // TODO display user list
        }
    });
}

function get_images() {
    $.ajax({
        type: 'GET',
        url: '/images/',
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(result){
            // TODO display images
            var act_reg = '';
            for(i = 0; i < result.images.length; ++i) {
                act_reg += create_image_post(result.images[i]);
            }
            $('#active-region').html(act_reg);
            console.log(result);
        }
    });
}

// helper functions:
function update_navbar() {
    $('nav #home').show();
    $('nav #waiting').show();
    var auth = user_is_authenticated(function() {
        $('nav #login').hide();
        $('nav #register').hide();
        $('nav #my').show();
        $('nav #logout').show();
    }, function() {
        $('nav #login').show();
        $('nav #register').show();
        $('nav #my').hide();
        $('nav #logout').hide();
    });
}

function user_is_authenticated(fun_success, fun_failure) {
    $.ajax({
        type: 'GET',
        url: '/auth/',
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(result) {
            if(result.result == 'ok')
                fun_success(result);
            else
                fun_failure(result);
        },
//        success: fun_success,
//        failure: fun_failure,
    });

}

function create_image_post(img) {
    var result = '<div class="image_post"><p>';
    result += img.title;
    result += '</p>';
    result += '<img src="' + img.url + '" />';
    result += '</div>';
    return result;
}

// page functions
function home() {
    get_images();
    update_navbar();
}

function waiting() {
    // TODO implement waiting room
}

function login() {
    // TODO implement login
}

function register() {
    // TODO implement register
}

function my() {
    // TODO implement my images
}

function logout() {
    // TODO implement logout
}

$(document).ready(function() {
    $('nav #home').click(home);
    $('nav #waiting').click(waiting);
    $('nav #login').click(login);
    $('nav #register').click(register);
    $('nav #my').click(my);
    $('nav #logout').click(logout);
    home();
});