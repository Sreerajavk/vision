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
                console.log(response.user_list);
                fill_table(response)
            }
        },
        fail: function (response) {

        }
    })
})
$(document.body).on('click', '.table-row', function (event) {

    // let option = $('#option_type').val();
    // alert(option)
    id = ($(this).attr('id'));
    // alert('sdfsdf')
    $.ajax({
        url: '/dashboard/get-analytics/',
        datatype: 'json',
        method: 'post',
        data: {
            id: id,
            type : 'day',
            camera_id:  'All cameras',
            org_id : $('#org_id').prop('value'),
        },
        success: function (response) {

            if (response.status == '200') {
                    fill_chart(response);
                    fill_timestamp(response)
                    console.log(response.data)
                     $('#user_id').prop('value' , response.data.id);
                    $('#no_content').removeClass('no-content');
                    $("#no_content").html("");
                    $('#analytic_head').html(response.data.name )
                $('#option_time').val('day');
                    $("#option_camera").val(response.camera_name)
            }
        },
        fail: function (response) {

        }
    })
})


$(document.body).on('click', '.options', function (event) {

    // let option = $('#option_type').val();
    // alert(option)
    let id = $('#user_id').prop('value');
    // alert(id)
    // alert('sdfsdf')
    // alert($('#org_id').prop('value'))
    $.ajax({
        url: '/dashboard/get-analytics/',
        datatype: 'json',
        method: 'post',
        data: {
            id: id,
            org_id : $('#org_id').prop('value'),
            type : $('#option_time').val(),
            camera_id : $('#option_camera').val()
        },
        success: function (response) {

            if (response.status == '200') {
                    fill_chart(response);
                    fill_timestamp(response);
                    $('#analytic_head').html(response.data.name )
            }
        },
        fail: function (response) {

        }
    })
})


function fill_table(response) {
    let table_content = document.getElementById('table_content');

    $('#full_table').slideUp(500, function () {
        table_content.innerHTML = "";
        for (user of response.user_list) {
            let row = `<tr id="${user.id}" class="table-row"><td>${user.count}</td><td>${user.name}</td><td><img src="${user.image_url}" id="table-image"></td><td>${user.privilege}</td></tr>`
            table_content.innerHTML += row;
        }
        $('#full_table').slideDown(500)
    })
}

function fill_chart(response) {
    var basic_chart = document.getElementById("basic-chart");
    basic_chart.innerHTML = "";
    basic_chart.innerHTML += `<canvas id="basiclinechart"></canvas>`;
    var ctx = document.getElementById("basiclinechart");
    var basiclinechart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: response.time_list,
            datasets: [{
                label: "Count",
                fill: true,
                backgroundColor: '#03a9f4',
                borderColor: '#03a9f4',
                data: response.count_list

            }]
        },
        options: {
            responsive: true,
            title: {
                display: false,
                text: 'Basic Line Chart'
            },
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [{
                    ticks: {
                        autoSkip: false,
                        maxRotation: 0
                    },
                    ticks: {
                        fontColor: "#fff", // this here
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Time'
                    }
                }],
                yAxes: [{
                    ticks: {
                        autoSkip: false,
                        maxRotation: 0
                    },
                    ticks: {
                        fontColor: "#fff", // this here
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Count'
                    }
                }]
            }
        }
    });
}

function fill_timestamp(response) {

    let table_content = document.getElementById('timestamp_content');

    // $('#full_table').slideUp(500, function () {
        table_content.innerHTML = "";
        for (user of response.raw_data) {
            let row = `<tr  class="table-row"><td>${user.count}</td><td>${user.date}</td><td>${user.time}</td><td>${user.camera_name}</td></tr>`
            table_content.innerHTML += row;
        }
        $('#analytiv_div').slideDown(500);
        $('#analytic_head2').html(response.data.name + "  Analytics")
    // })

}