// $(function () {
//     /* 1. OPEN THE FILE EXPLORER WINDOW */
//     $(".js-upload-photos").click(function () {
//         $("#fileupload").click();
//     });
//
//       /* 2. INITIALIZE THE FILE UPLOAD COMPONENT */
//   $("#fileupload").fileupload({
//     dataType: 'json',
//     done: function (e, data) {  /* 3. PROCESS THE RESPONSE FROM THE SERVER */
//       if (data.result.is_valid) {
//         $("#gallery tbody").prepend(
//           "<tr><td><a href='" + data.result.url + "'>" + data.result.name + "</a></td></tr>"
//         )
//       }
//     }
//   });
// });


$('#candidate_form1').submit(function (event) {

    event.preventDefault();
    let data = $('#candidate_form1').serialize();
    console.log(data)

    $('#next_step').html('Sending  <img src="/static/images/spinner2.gif" style="width: 30px;height: 30px;">');


    $.ajax({
        url: '/dashboard/add-candidates/',
        method: 'post',
        datatype: 'json',
        data: data,
        success: function (response) {

            // alert(response.status)

            if (response.status == '200') {
                // alert('success');
                let user_id = response.user_id;
                let csrf_token = $('input[name=csrfmiddlewaretoken]').val()
                console.log(user_id , csrf_token);
                // $('#fileupload').prop('data-form-data' , '{"csrfmiddlewaretoken": "'+ csrf_token+'","user_id" :"'+ user_id +'"}')
                document.getElementById('fileupload').setAttribute('data-form-data' , '{"csrfmiddlewaretoken": "'+ csrf_token+'","user_id" :"'+ user_id +'" , "edit" : "false"}')
                // console.log(($('#fileupload').prop('data-form-data')))
                $('#warning_text').html('User created Successfully');
                $('#alert').removeClass('alert-danger');
                $('#alert').addClass('alert-success')
                $('#alert').css('display', 'block');
                // $('#send_bt').html('Send Invite Link');
                setTimeout(function () {
                    $('#alert').css('display', 'none');
                }, 4000)

                // setTimeout()

                $('#div1').slideUp(1000 ,function () {
                    $('#div2').slideDown(1000);
                });


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