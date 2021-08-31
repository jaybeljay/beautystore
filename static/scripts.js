$(document).ready(function(){
	function getCookie(name) {
		let cookieValue = null;
		if (document.cookie && document.cookie !== '') {
			const cookies = document.cookie.split(';');
			for (let i = 0; i < cookies.length; i++) {
				const cookie = cookies[i].trim();
				if (cookie.substring(0, name.length + 1) === (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}
	const csrf_token = getCookie('csrftoken');
	var form = $('#form_buying_prod');
	form.on('submit', function(e){
		e.preventDefault();
		var nmb = $('#quantity').val();
		var submit_btn = $('#submit_btn');
		var product_id = submit_btn.data('product_id');
		var product_name = submit_btn.data('name');
		var product_price = submit_btn.data('price');
		
		var data={};
		data.product_id = product_id;
		data.nmb = nmb;
		data['csrfmiddlewaretoken'] = csrf_token;
		var url = form.attr('action');
		
		$.ajax({
			url: url,
			type: 'POST',
			data: data,
			cache: true,
			success: function (json) {
				if (json.products_total_nmb){
					$('#cart_products').find('[data-count="cart"]').text(json.products_total_nmb);
					$('.cart').closest('i').remove();
					$('.cart ul').html("");
					$.each(json.products, function(k, v){
						$('.cart ul').append('<li>' + v.name + ', ' + v.nmb + 'pcs. ' + '- ' + v.price + '<button type="button" class="btn-close" aria-label="Delete"></button>' + '</li>');
					})
				}
			},
			error: function(){
				console.log('error');
			}
		})
	})
	
	$(document).on('click', '.btn-close', function(e) {
		e.preventDefault();
		var url = $(this).attr('href');
		var item_id = $(this).data('id');
		var item_type = $(this).data('type');
		console.log(item_id);
		console.log(item_type);
		
		var data = {};
		data['item_id'] = item_id;
		data['item_type'] = item_type;
		data['csrfmiddlewaretoken'] = csrf_token;
		console.log(data);
		
		$.ajax({
			url: url,
			type: 'POST',
			beforeSend: function(xhr) {
				xhr.setRequestHeader('X-CSRFToken', csrf_token);
			},
			dataType: 'json',
			сontentType: 'application/json; charset=utf-8',
			processData: false,
			data: JSON.stringify({'item_id': item_id, 'item_type': item_type}),
			success: function(json) {
				$('.btn-close').closest('li').remove();
			},
			error: function(){
				console.log('error');
			}
		})
	})
	
	function calculatingCartAmount() {
		var total_order_amount = 0;
		$('.total_product_in_cart_amount').each(function(){
			total_order_amount += parseInt($(this).text());
		});
		$('#total_order_amount').text(total_order_amount);
	};
	
	$(document).on('change', ".product_in_cart_nmb", function(){
		var current_nmb = $(this).val();
		var current_tr = $(this).closest('tr');
		var current_price = parseInt(current_tr.find('.product_price').text());
		var total_amount = current_nmb*current_price
		current_tr.find('.total_product_in_cart_amount').text(total_amount);
		calculatingCartAmount();
	})
	
	calculatingCartAmount();
	
	$(document).on('click', '#favorite_btn', function() {
		var product_id = $(this).data('product_id');
		var name = $(this).data('name');
		var price = $(this).data('price');
		var url = $('#favorite_btn').attr('href');
		
		$.ajax({
			url: url,
			type: 'POST',
			data: {'obj': product_id, 'csrfmiddlewaretoken': csrf_token},
			success: function(json) {
				console.log('OK');
				console.log(json.favorites_nmb);
				console.log(json.favorites);
				$('#favorite_products').find('[data-count="favorite"]').text(json.favorites_nmb);
				$('.favorite-cart').closest('span i').remove();
				$('.favorite-cart ul').html("");
				$.each(json.favorites, function(k, v){
					$('.favorite-cart ul').append('<li>' + v.name + '- ' + v.price + '<button type="button" class="btn-close" aria-label="Delete"></button>' + '</li>');
				})
			}
		});
		
		return false;
		
	})
});