$(document).ready(function () {

    $(".zero").on('keyup', function (event) {
        var value = $(this).val();
        if (!value.startsWith('+98')) {
            $(this).val("+98");
        }
    });

    $("#like").click( function () {
        let url_like=$(this).data('url');
        $.post({
            url:url_like,
            success:function (result){
                alert(result);
            }
        });
    });


});


