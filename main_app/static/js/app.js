$(document).ready(function() {

	function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie !== '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) === (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}

	var csrftoken = getCookie('csrftoken');

	function csrfSafeMethod(method) {
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}

	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		}
	})

	$("a.pop-up").on("click", function() {
       $('#imagepreview').attr('src', $(this).find('#imageresource').attr('data-url'));
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
	
	$(".favorite-button").on('click', function (event) {

		event.preventDefault();
		var el = $(this);
		el.blur();
		el.addClass("disabled");
		$.ajax({
			url: '/favorite_product/',
			type: 'POST',
			data: {product_id: el.attr("data-id")},
			dataType: 'json',
			success : function (data) {
				el.removeClass("disabled");
				el.toggleClass("btn-secondary");
				el.toggleClass("btn-warning");
			},

			error: function (data) {
				el.removeClass("disabled");
			}
		});
	});

	$(".like-button").on('click', function (event) {
		event.preventDefault();
		var el = $(this);
		el.blur();
		el.addClass("disabled");
		$.ajax({
			url: '/like_product/',
			type: 'POST',
			data: {product_id: el.attr('data-id')},

			success: function (data) {
				el.removeClass('disabled');
				el.toggleClass('btn-secondary');
				el.toggleClass('btn-danger');
				if (data['likes'] == 0) {
					el.find('small').text('')
				} else {
					el.find('small').text(data['likes'])
				}
			},

			error: function (response) {
				el.removeClass("disabled");
			}
		});
	});
});
