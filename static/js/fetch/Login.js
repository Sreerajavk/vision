
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
        // {
        //     username : username,
        //     password : password,
        //     csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken]').val()
        // },
        // data : {
        //         org_name : org_name,
        //         location : location,
        //         email : email,
        //         username : username,
        //         first_name : first_name,
        //         last_name : last_name,
        //         password : password,
        //         phone_no : phone_no,
        //         image : formData,
        //         csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken]').val()
        // },
        // contentType: false,
        // cache: false,
        // processData: false,
        success: function (response) {

            // alert(response.status)

            if (response.status == '200') {
                window.location = '/dashboard'
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