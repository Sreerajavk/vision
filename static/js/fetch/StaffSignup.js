$('#staff_form').submit(function (event) {

    event.preventDefault();
    let password = $('#password').val();
    let confirm_password = $('#confirm_password').val();
    $form = $(this);
    let formData = new FormData(this);
    console.log(formData);

    if (password != confirm_password) {
        alert('Pasword does not match');
        return
    }
    //
    // let data = $('#org_form2').serialize();
    //
    // console.log(data)

    $('#register_bt').html('Signing Up <img src="/static/images/spinner2.gif" style="width: 30px;height: 30px;">');

    $.ajax({
        url: '/staff-signup/',
        method: 'post',
        data: formData,
        // datatype : 'json',
        contentType: false,
        cache: false,
        processData: false,
        success: function (response) {

            // alert(response.status)

            if(response.status == '200'){
                $('#sucess_model').modal('show');
                let time = 5;
                setInterval(function () {
                        if(time == 0 ){
                            window.location = '/'
                            clearInterval()
                        }
                        else{
                            time -=1;
                            $('#time').html(time);
                        }
                },1000)
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