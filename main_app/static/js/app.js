$(document).ready(function() {
   $("a.pop-up").on("click", function() {
       $('#imagepreview').attr('src', $(this).find('#imageresource').attr('src'));
       $('#imagemodal').modal('show');
    });

    $(".fancybox-thumb").fancybox({
		prevEffect	: 'none',
		nextEffect	: 'none',
		helpers	: {
			title	: {
				type: 'outside'
			},
			thumbs	: {
				width	: 50,
				height	: 50
			}
		}
	});

	$(".fancybox").fancybox();
});
