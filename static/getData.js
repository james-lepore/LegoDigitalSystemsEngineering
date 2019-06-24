function myFunction() {
	var input = document.getElementById("file");
	var file = input.files[0];
	if (!file) {
		return;
	}
	var reader = new FileReader();

	reader.onload = function(e) {
		var file_data = e.target.result;
	    console.log(file_data);

	    $.ajax({
	        data : {
	          contents : file_data
	        },
	        type : 'POST',
	        url : '/request'
	    }).done(function(data) {
	    	console.log(data)
	        document.getElementById("bob").innerHTML = "Success";
	    });
	};
	reader.readAsText(file);
	
}
