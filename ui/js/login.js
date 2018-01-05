$("#login-button").click(function() {
    data = {
        'email': $('#email').val(),
        'password': $('#password').val()
    };

    console.log(data);

    $.ajax({
        type: "POST",
        url: '/api/users/login',
        data: JSON.stringify(data),
        contentType:  'application/json; charset=utf-8',
        processData: false,
        success: function(response) {
            window.location.replace('/index.html');
        },
        error: function(response) {
            alert(response.responseText);
        },
    });
});
