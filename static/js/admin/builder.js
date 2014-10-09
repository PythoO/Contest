hide_div = function(){
    $('.field_option_form > div').hide();
}

hide_div();

$('.add_field').change(function() {
    var type = $(".add_field option:selected").val();
     hide_div();
     if (type == 'text'){
        $('.text_options').show();
    }
});

