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
            console.log(result);
        }
    });
}

// helper functions:
function update_navbar() {
    $('nav #home').show();
    $('nav #waiting').show();
    var auth = user_is_authenticated();

    if(!auth)
    {
        $('nav #login').show();
        $('nav #register').show();
        $('nav #my').hide();
    }
    else
    {
        $('nav #login').hide();
        $('nav #register').hide();
        $('nav #my').show();
    }
}

function user_is_authenticated() {
    $.ajax({
        type: 'GET',
        url: '/auth/',
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(result){
            return result.result == 'ok';
        }
    });
}

function home() {
    get_images()
}

$(document).ready(function() {
    update_navbar();
    $('nav #home').click(home);
    home();
});