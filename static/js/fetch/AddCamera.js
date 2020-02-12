

$('#camera_form').submit(function (event) {

    event.preventDefault();
    let data = $('#camera_form').serialize();
    console.log(data)
    $('#send_bt').html('Adding Camera  <img src="/static/images/spinner2.gif" style="width: 30px;height: 30px;">');


    $.ajax({
        url: '/dashboard/add-camera/',
        method: 'post',
        datatype: 'json',
        data: data,
        success: function (response) {

            // alert(response.status)

            if (response.status == '200') {

                $('#warning_text').html('Camera Added  Successfully');
                $('#alert').removeClass('alert-danger');
                $('#alert').addClass('alert-success')
                $('#alert').css('display', 'block');
                // $('#send_bt').html('Send Invite Link');
                setTimeout(function () {
                    $('#alert').css('display', 'none');
                }, 4000)
    $('#send_bt').html('Add Camera <i class="fas fa-video"></i>');


            } else {
                // alert('failed')
                  $('#alert').removeClass('alert-success');
                $('#alert').addClass('alert-danger')
                $('#warning_text').html('Username already exists')
                $('#alert').css('display', 'block')
                    $('#next_step').html('Next Step');


                // $('#login_bt').html('Login');
                // $('#send_bt').html('Send Invite Link');
            }
        },
        fail: function (response) {

        }

    })


});