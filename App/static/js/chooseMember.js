$(document).ready(function(){
	$('input.autocomplete').autocomplete({
		// Must show all users from BD
		data: {
			"Sergio Sanchez": null,
			"Enrike Ramos": null,
			"Abigail Nicolas": null
		},
	});
});

$(document).ready(function(){
	$('input.inCharge').autocomplete({
		// Must show all users from BD
		data: {
			"Sergio Sanchez": null
		},
	});
});
