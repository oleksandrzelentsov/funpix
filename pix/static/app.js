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

function get_images(my=false) {
    $.ajax({
        type: 'GET',
        url: (!my) ? '/images/' : '/images?my',
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(result) {
            var act_reg = '';
            for(i = 0; i < result.images.length; ++i) {
                act_reg += create_image_post(result.images[i]);
            }
            $('#active-region').html(act_reg);
            for(i = 0; i < result.images.length; ++i) {
                $('#like' + result.images[i].pk).click(function(e) {
                    $.ajax({
                        type: 'GET',
                        url: '/images/' + e.target.id.replace('like', '') + '/plus/',
                        contentType: "application/json; charset=utf-8",
                        dataType: "json",
                        success: function(result) {
                            $(e.target).val('+ (' + result.likes + ')');
                            // get_images();
                        },
                    });
                });
            }
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
        $('nav #add').show();
    }, function() {
        $('nav #login').show();
        $('nav #register').show();
        $('nav #my').hide();
        $('nav #logout').hide();
        $('nav #add').hide();
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
    result += '<img src="' + img.url + '" /><br>';
    var temp = img.url.split('/');
    result += '<input type="button" id="like' + temp[temp.length - 1] + '" type="button" value="+ (' + img.likes + ')"/><br>';
    result += 'by ' + img.user;
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
    get_images(true);
    update_navbar();
}

function logout() {
    // TODO implement logout
}

function add_image() {
    // TODO implement add image
}

$(document).ready(function() {
    $('nav #home').click(home);
    $('nav #waiting').click(waiting);
    $('nav #login').click(login);
    $('nav #register').click(register);
    $('nav #my').click(my);
    $('nav #logout').click(logout);
    $('nav #add').click(add_image);
    home();
});