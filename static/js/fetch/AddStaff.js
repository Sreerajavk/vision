$('#staff_form').submit(function (event) {

    event.preventDefault();
    let data = $('#staff_form').serialize();
    console.log(data)

    $('#send_bt').html('Sending  <img src="/static/images/spinner2.gif" style="width: 30px;height: 30px;">');


    $.ajax({
        url: '/dashboard/add-staff/',
        method: 'post',
        datatype: 'json',
        data: data,
        success: function (response) {

            // alert(response.status)

            if (response.status == '200') {
                $('#warning_text').html('Email Send Successfully');
                $('#alert').css('display' , 'block');
                $('#send_bt').html('Send Invite Link');
                setTimeout(function () {
                     $('#alert').css('display' , 'none');
                }, 4000)
            } else {
                $('#warning_text').html('Something went wrong')
                $('#alert').css('display' , 'block')
                $('#login_bt').html('Login');
                $('#send_bt').html('Send Invite Link');
            }
        },
        fail: function (response) {

        }

    })

});