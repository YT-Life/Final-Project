$(document).ready(function() {
    $('#loading').hide();
    $('#loadingbtn').click(function(){
        $('#loadingbtn').hide();
        $('#loading').show();
      
        return true;
    });
});