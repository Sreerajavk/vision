$(document.body).on('click', '#option_type', function (event) {

    let option = $('#option_type').val();
    // alert(option)
    $.ajax({
        url: '/dashboard/filter-type/',
        datatype: 'json',
        method: 'post',
        data: {
            option: option
        },
        success: function (response) {

            if (response.status == '200') {
                console.log(response.user_list)
                let table_content = document.getElementById('table_content');

                $('#full_table').slideUp(500, function () {
                    table_content.innerHTML = "";
                    for (user of response.user_list) {
                        let row = `<tr id="row${user.id}" class="table-row"><td>${user.count}</td><td>${user.name}</td><td><img src="${user.image_url}" id="table-image"></td><td>${user.privilege}</td>`
                        table_content.innerHTML += row;
                    }
                    $('#full_table').slideDown(500)
                })

            }
        },
        fail: function (response) {

        }
    })
})