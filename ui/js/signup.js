$("#signup-button").click(function() {
    console.log("Hello");
    data = {
        'name': $('#name').val(),
        'email': $('#email').val(),
        'shipping_address': $('#shipping-adress').val(),
        'password': $('#password').val()
    };

    console.log(data);

    $.ajax({
        type: "POST",
        url: '/api/users/signup',
        data: JSON.stringify(data),
        contentType:  'application/json; charset=utf-8',
        processData: false,
        success: function(response) {
            window.location.replace('/login.html');
        },
        error: function(response) {
            alert(response.responseText);
        },
    });
});
