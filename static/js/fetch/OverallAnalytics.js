

$(document.body).on('click' , '#search_bt' , function (event) {
    event.preventDefault();
    let from_date = $("#from_date").val();
    let to_date = $('#to_date').val();
    if(from_date == ""){
        alert('Select from date');
        return
    }
    if(to_date == ""){
        alert('Select to date');
        return
    }

    $.ajax({
        url : '/dashboard/overall-analytics/',
        method : 'post',
        datatype : 'json',
        data : {
            from_date  : from_date,
            to_date : to_date,
            org_id : $('#org_id').prop('value'),
            type : 'All'
        },
        success : function (response) {
            // alert('sjhfdksjdh')
            fill_chart(response);
            fill_table(response)
        },
        fail : function (response) {

        }

    })

});

$(document.body).on('click', '#option_type', function (event) {

    let option = $('#option_type').val();
    // alert(option)
    $.ajax({
        url: '/dashboard/overall-analytics/',
        datatype: 'json',
        method: 'post',
        data: {
            from_date  : from_date,
            to_date : to_date,
            org_id : $('#org_id').prop('value'),
            type : option
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


function fill_table(response) {
    let data = response.data;
    console.log(data)
     let table_content = document.getElementById('table_content');

    // $('#full_table').slideUp(500, function () {
        table_content.innerHTML = "";
        for (user of response.data) {
            let row = `<tr id="${user.id}" class="table-row"><td>${user.count}</td><td>${user.name}</td><td><img src="${user.image_url}" id="table-image"></td><td>${user.type}</td><td>${user.count}</td></tr>`
            table_content.innerHTML += row;
        }
        $('#full_content').slideDown(500)
    // })
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