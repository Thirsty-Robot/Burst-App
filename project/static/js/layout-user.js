$(document).ready(function(){
    var hidden = 1;

    $(".notification").hide();

    $("#notification").click(function(){
        if (hidden == 1) {
            $(".notification").show();
            hidden = 0;
        }
        else if (hidden == 0) {
            $(".notification").hide();
            hidden = 1;
        }
    });
});