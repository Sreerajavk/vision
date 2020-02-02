$('#search_form').submit(function (event) {

    event.preventDefault();
    let data = $('#search_form').serialize();
    console.log(data);

    let option = $('#option').val()
    // if(option )
    if (option == "Select") {
        alert('Plase select an option');
        return
    }
    $('#search_bt').html('Searching  <img src="/static/images/spinner2.gif" style="width: 30px;height: 30px;">');

    $.ajax({
        url: '/dashboard/manage/',
        method: 'post',
        datatype: 'json',
        data: data,
        success: function (response) {

            // alert(response.status)

            if (response.status == '200') {

                // console.log(response.data)
                $('#search_bt').html('Search <i class="fas fa-search"></i>');

                let table_content = document.getElementById('table_content');
                table_content.innerHTML = "";

                // alert(Object.size(response.data))
                if (Object.entries(response.data).length == 0) {
                    // $('#div_head').html("No Available data");
                    // $('table').css('display', 'none');
                    $('#div2').slideUp(1000, function () {
                        $('#no_content').slideDown(1000);
                    });

                    return
                }
                let edit_id;
                $('#div2').slideUp(1000, function () {
                    if (response.flag == 1) {
                        $('#div_head').html('Staff list');
                    } else {
                        $('#div_head').html('Candidate list');
                    }
                });
                // $('table').css('display', 'block');
                for (let id in response.data) {

                    let user = response.data[id]
                    console.log(user)
                    let username = user.username
                    let name = user.first_name + ' ' + user.last_name
                    let image_url = user.image_url
                    let phone = user.phone;
                    let delete_id;
                    let manage;
                    // let email = user.email
                    if (response.flag == 1) {
                        edit_id = "edit!staff!" + id;
                        delete_id = "delete!staff!" + id;
                        manage = `<td><button data-toggle="tooltip" title="Trash" class="pd-setting-ed delete_bt" id="${delete_id}"><i class="far fa-trash-alt" aria-hidden="true" style="color: #f00;"></i></button></td></tr>`

                    } else {
                        edit_id = "edit!candidate!" + id;
                        delete_id = "delete!candidate!" + id;
                        manage = `<td><button data-toggle="tooltip" title="Edit" class="pd-setting-ed edit_bt" id="${edit_id}" ><i class="far fa-edit" aria-hidden="true" style="color: #0f0;"></i></button>` +
                        ` <button data-toggle="tooltip" title="Trash" class="pd-setting-ed delete_bt" id="${delete_id}"><i class="far fa-trash-alt" aria-hidden="true" style="color: #f00;"></i></button></td></tr>`

                    }

                    let row = `<tr id="row${id}"><td><img src="${user.image_url}"></td><td>${name}</td><td>${username}</td><td>${phone}</td>` + manage

                    table_content.innerHTML += row;
                }
                $('#no_content').slideUp(1000, function () {
                    $('#div2').slideDown(1000);
                });


            } else {

            }
        },
        fail: function (response) {

        }

    })
});

$(document.body).on('click', '.edit_bt', function (event) {

    event.preventDefault();
    let type = $(this).attr('id').split('!')[1]
    let id = $(this).attr('id').split('!')[2]

    if (type == 'candidate') {
        // alert('sldkfjl')
        window.location = '/dashboard/edit-candidate/' + id;
    }

    // alert(id)
    // window.location = '/dashboard/'
})

let type;
let id;

$(document.body).on('click', '.delete_bt', function (event) {

    event.preventDefault();
    console.log($(this).attr('id'));
    type = $(this).attr('id').split('!')[1]
    id = $(this).attr('id').split('!')[2]
    // alert(id)
    // window.location  = '/dashboard/'
    $('#delete-model').modal('show');
    $('.delete-item').attr('id', 'delete@' + id);
});


$(document.body).on('click', '.delete-item', function (event) {

    $('#delete-model').modal('hide');
    // alert(type )
    if (type == 'candidate') {
        type = 0;
    } else {
        type = 1;
    }
    // alert(id)
    $.ajax({
        url: '/dashboard/delete-staff/',
        method: 'post',
        datatype: 'json',
        data: {
            user_id: id,
            type: type,
            org_id: $('#org_id').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function (response) {

            let id = response.id;
            let length = response.length;
            if (length == 0) {
                $('#div2').slideUp(1000, function () {
                    $('#no_content').slideDown(1000);
                });
                return;
            }
            // alert('#row' + id)
            $('#row' + id).fadeOut()

        },
        fail: function (response) {

        }
    });
})