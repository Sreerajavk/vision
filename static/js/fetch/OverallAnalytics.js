$(document.body).on('click', '#search_bt', function (event) {
    event.preventDefault();
    let from_date = $("#from_date").val();
    let to_date = $('#to_date').val();
    if (from_date == "") {
        alert('Select from date');
        return
    }
    if (to_date == "") {
        alert('Select to date');
        return
    }
    $('#search_bt').html('Searching  <img src="/static/images/spinner2.gif" style="width: 30px;height: 30px;">');

    $.ajax({
        url: '/dashboard/overall-analytics/',
        method: 'post',
        datatype: 'json',
        data: {
            from_date: from_date,
            to_date: to_date,
            org_id: $('#org_id').prop('value'),
            type: 'All',
            camera_id: 'All'
        },
        success: function (response) {
            // alert('sjhfdksjdh')
            fill_chart(response);
            fill_table(response, true);
            $('#search_bt').html('Search<i class="fas fa-search"></i>');


        },
        fail: function (response) {
            $('#search_bt').html('Search<i class="fas fa-search"></i>');
        }

    })

});

$(document.body).on('change', '.option', function (event) {

    event.preventDefault();
    let from_date = $("#from_date").val();
    let to_date = $('#to_date').val();
    if (from_date == "") {
        alert('Select from date');
        return
    }
    if (to_date == "") {
        alert('Select to date');
        return
    }
    let type = $('#option_type').val();
    let camera_id = $('#option_camera').val();
    console.log(type, camera_id)
    $.ajax({
        url: '/dashboard/overall-analytics/',
        datatype: 'json',
        method: 'post',
        data: {
            from_date: from_date,
            to_date: to_date,
            org_id: $('#org_id').prop('value'),
            type: type,
            camera_id: camera_id,
        },
        success: function (response) {

            if (response.status == '200') {
                console.log(response.data);
                fill_table(response, false);
                fill_chart(response)
            }
        },
        fail: function (response) {

        }
    })
})


function fill_table(response, status) {
    let data = response.data;
    console.log(data);
    let table_content = document.getElementById('table_content');
    // if (!status) {
    //     // alert('sdf')
    //     $('#table_content').slideUp(1000, function () {
    //         table_content.innerHTML = "";
    //         for (user of response.data) {
    //             let row = `<tr id="${user.id}" class="table-row"><td>${user.count}</td><td>${user.name}</td><td><img src="${user.image_url}" id="table-image"></td><td>${user.type}</td><td>${user.count}</td></tr>`
    //             table_content.innerHTML += row;
    //         }
    //
    //         $('#table_content').slideDown(500);
    //     })
    // }
    //     else {
    //          table_content.innerHTML = "";
    //         for (user of response.data) {
    //             let row = `<tr id="${user.id}" class="table-row"><td>${user.count}</td><td>${user.name}</td><td><img src="${user.image_url}" id="table-image"></td><td>${user.type}</td><td>${user.count}</td></tr>`
    //             table_content.innerHTML += row;
    //         }
    //         $('#full_content').slideDown(500);
    //     }
    if (status) {

        // $('#full_table').slideUp(500, function () {
        table_content.innerHTML = "";
        for (user of response.data) {
            let row = `<tr id="${user.id}" class="table-row"><td>${user.no}</td><td>${user.name}</td><td><img src="${user.image_url}" id="table-image"></td><td>${user.type}</td><td>${user.count}</td></tr>`
            table_content.innerHTML += row;
        }

        $('#full_content').slideDown(500);
        // })
    } else {
        $('#full_content').slideDown(500);
        $('#full_table').slideUp(500, function () {
            table_content.innerHTML = "";
            for (user of response.data) {
                let row = `<tr id="${user.id}" class="table-row"><td>${user.no}</td><td>${user.name}</td><td><img src="${user.image_url}" id="table-image"></td><td>${user.type}</td><td>${user.count}</td></tr>`
                table_content.innerHTML += row;
            }

            $('#full_table').slideDown(500);
        })
    }


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