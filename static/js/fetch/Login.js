
$('#login_form').submit(function (event) {

    event.preventDefault();
    console.log('form')
    let username = $('#username').val();
    let password = $('#password').val();

    let data = $('#login_form').serialize();
    //
    console.log(data);

    $('#login_bt').html('Logging In <img src="/static/images/spinner2.gif" style="width: 30px;height: 30px;">');


    $.ajax({
        url: '/login/',
        method: 'post',
        datatype : 'json',
        data: data,
        success: function (response) {

            // alert(response.status)

            if (response.status == '200') {
                window.location = '/dashboard/'
            } else if(response.status == '300') {
                $('#warning_text').html('Unauthorised Access')
                $('#alert').css('display', 'block')
                $('#login_bt').html('Login');
            }
            else{
                $('#warning_text').html('Invalid username or password')
                $('#alert').show();
                $('#login_bt').html('Login');
            }
        },
        fail: function (response) {

        }

    })

});