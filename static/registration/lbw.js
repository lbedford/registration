function ShowElementWhenButtonClicked(button_id, element_id) {
  $(button_id).click(function() {
    $(element_id).show();
  });
}

function HideElementWhenButtonClicked(button_id, element_id) {
  $(button_id).click(function() {
    $(element_id).hide();
  });
}

function SetupDeleteHandler(button_id) {
  $(button_id).click(function() {
    $.ajax({
	type: 'POST',
	url: $(button_id).attr('data-url'),
	data: {
	    csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
	},
	success: function(data) {
	  location.reload(true);
	},
	error: function(xhr, textStatus, errorThrown) {
	  alert("Please report this error: "+errorThrown+xhr.status+xhr.responseText);
	}
    });
  });
}

$(function() {
  $( ".datepicker" ).datepicker({dateFormat: "yy-mm-dd"});
});

$(function() {
  $( ".datetimepicker" ).datetimepicker({dateFormat: "yy-mm-dd"});
});
