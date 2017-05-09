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
                act_reg += '<div class="image-post"><p>' + result.images[i].title + '</p><img src="' + result.images[i].url + '" /></div>';
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
    }, function() {
        $('nav #login').show();
        $('nav #register').show();
        $('nav #my').hide();
    });
}

function user_is_authenticated(fun_success, fun_failure) {
    $.ajax({
        type: 'GET',
        url: '/auth/',
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: fun_success,
        failure: fun_failure,
    });

}

function home() {
    get_images();
    update_navbar();
}

$(document).ready(function() {
    $('nav #home').click(home);
    home();
});