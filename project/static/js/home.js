$(document).ready(function(){
    $('.like').mouseover(function(){
        $('.like').hide();
        $('.liked').show();
    });

    $('.liked').mouseout(function(){
        $('.liked').hide();
        $('.like').show();
    });
});