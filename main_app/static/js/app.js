$(document).ready(function() {
   $("a.pop-up").on("click", function() {
       $('#imagepreview').attr('src', $(this).find('#imageresource').attr('src'));
       $('#imagemodal').modal('show');
    });
});
