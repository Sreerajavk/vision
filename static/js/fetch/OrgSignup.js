$('#org_form2').submit(function (event) {

    event.preventDefault();
    console.log('form')
    let email = $("#email").val();
    let org_id = $('#org_id').val()
    let username = $('#username').val();
    let first_name = $('#first_name').val();
    let last_name = $('#last_name').val();
    let password = $('#password').val();
    let confirm_password = $('#confirm_password').val();
    let phone_no = $('#phone_no').val();
    $form = $(this);
    let formData = new FormData(this);
    console.log(formData);

    console.log(email , org_id)

    // let image = $('#image').prop('files');
    // console.log(image)
    // console.log(password, confirm_password)
    // console.log(org_name, location, email, username, first_name, last_name)

    if (password != confirm_password) {
        alert('Pasword does not match');
        return
    }

    let data = $('#org_form2').serialize();

    console.log(data)

    $('#register_bt').html('Signing Up <img src="/static/images/spinner2.gif" style="width: 30px;height: 30px;">');

    $.ajax({
        url: '/org-signup/',
        method: 'post',
        data: formData,
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
        // datatype : 'json',
        contentType: false,
        cache: false,
        processData: false,
        success: function (response) {

            // alert(response.status)

            if(response.status == '200'){
                window.location = '/login'
            }
            else{
                $('#warning_text').html('Username already exists')
                $('#alert').show();
                $('#register_bt').html('Register');
            }
        },
        fail: function (response) {

        }

    })

});

$('#next_step').click(function (event) {
    let org_name = $('#org_name').val();
    let location = $('#location').val();
    let email = $('#email').val()

    $.ajax({
        url: '/add-organisation/',
        dataType: 'json',
        data: {
            org_name: org_name,
            location: location
        },
        method: 'post',
        success: function (response) {
                // alert(response.id)
            $('#option2').prop('checked', 'true');
                $('#email_new').prop('value' , email)
                $('#org_id').prop('value' , response.id)
        },
        fail: function (response) {

        }

    })


})