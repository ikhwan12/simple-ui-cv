$(document).ready(function () {
    const previewFile = function (input){
        let file = $(input).get(0).files[0]
        if(file){
            let reader = new FileReader()
            reader.onload = function(){
                $("#input-img").attr("src", reader.result)
            }
            reader.readAsDataURL(file)
        }
    }

    $('#input-file').change(function (e) { 
        e.preventDefault();
        previewFile(this)
    });

    $('#processBtn').click(function (e) { 
        e.preventDefault();

        let formData = new FormData($('#segForm')[0])

        $.ajax({
            type: "POST",
            url: $('#segForm').attr('action'),
            data: formData,
            dataType: "JSON",
            contentType: false,
            processData: false,
            success: function (response) {
                let dataSrc = "data:image/"+response.format+";base64, "+response.img
                $("#result-img").attr("src", dataSrc)
            },
            error: function (req, status, error) {
                alert(req.responseJSON.msg)
            }
        });
    });
});