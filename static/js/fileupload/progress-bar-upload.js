$(function () {

    $(".js-upload-photos").click(function () {
        $("#fileupload").click();
    });


});
$('#fileupload').click(function () {
    $("#fileupload").fileupload({
        dataType: 'json',
        sequentialUploads: true,

        start: function (e) {
            // alert('start')
            $("#modal-progress").modal("show");

        },

        stop: function (e) {
            // alert('stop')
            $("#modal-progress").modal("hide");
        },

        progressall: function (e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            var strProgress = progress + "%";
            $(".progress-bar").css({"width": strProgress});
            $(".progress-bar").text(strProgress);
        },

        done: function (e, data) {
            // alert('sdfsdf')
            console.log(data.formData.edit)
            // if (data.status == 200) {
            let edit = data.formData.edit;
            if (edit == 'true')
                window.location = '/dashboard/manage/?status=true';
            else
                window.location = '/dashboard/add-candidates/?status=true';
            // }


            // if (data.result.is_valid) {
            //   $("#gallery tbody").prepend(
            //     "<tr><td><a href='" + data.result.url + "'>" + data.result.name + "</a></td></tr>"
            //   )
            // }
        }

    });
});


