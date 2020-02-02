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
    let id = $('#id').val();

    $.ajax({
        url: '/dashboard/edit-candidate/' + id,
        method: 'post',
        datatype: 'json',
        data: data,
        success: function (response) {

            // alert(response.status)

            if (response.status == '200') {
                // alert('success');
                let user_id = response.user_id;
                let csrf_token = $('input[name=csrfmiddlewaretoken]').val()
                console.log(user_id, csrf_token);
                // $('#fileupload').prop('data-form-data' , '{"csrfmiddlewaretoken": "'+ csrf_token+'","user_id" :"'+ user_id +'"}')
                document.getElementById('fileupload').setAttribute('data-form-data', '{"csrfmiddlewaretoken": "' + csrf_token + '","user_id" :"' + user_id + '"}')
                // console.log(($('#fileupload').prop('data-form-data')))
                $('#warning_text').html('User information updated Successfully');
                $('#alert').removeClass('alert-danger');
                $('#alert').addClass('alert-success')
                $('#alert').css('display', 'block');
                // $('#send_bt').html('Send Invite Link');
                setTimeout(function () {
                    $('#alert').css('display', 'none');
                }, 4000)

                // setTimeout()

                document.getElementById('fileupload').setAttribute('data-form-data', '{"csrfmiddlewaretoken": "' + csrf_token + '","user_id" :"' + user_id + '" , "edit" : "true"}')

                let table_content = document.getElementById('table_content');
                table_content.innerHTML = "";
                for (let pic of response.pic_list) {
                    let row = `<tr id="row${pic.id}"><td>${response.name}</td><td><img src="${pic.image_url}"/></td><td>${pic.image_url}</td>` +
                        ` <td><button data-toggle="tooltip" title="Trash" class="pd-setting-ed delete_bt" id="delete!${pic.id}"><i class="far fa-trash-alt" aria-hidden="true" style="color: #f00;"></i></button></td></tr>`;

                    table_content.innerHTML += row;
                }
                $('#div1').slideUp(1000, function () {
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

let id;
$(document.body).on('click', '.delete_bt', function (event) {

    event.preventDefault();
    console.log($(this).attr('id'));
    id = $(this).attr('id').split('!')[1]
    $('#delete-model').modal('show');
    $('.delete-item').attr('id', 'delete@' + id);
});


$(document.body).on('click', '.delete-item', function (event) {

    $('#delete-model').modal('hide');
    $.ajax({
        url: '/dashboard/delete-images/',
        method: 'post',
        datatype: 'json',
        data: {
            id: id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function (response) {

            let id = response.id;
            // let length = response.length;
            // if (length == 0) {
            //     $('#div2').slideUp(1000, function () {
            //         $('#no_content').slideDown(1000);
            //     });
            //     return;
            // }
            // alert('#row' + id)
            $('#row' + id).fadeOut()

        },
        fail: function (response) {

        }
    });
})