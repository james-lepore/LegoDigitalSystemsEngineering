function myFunction() {
	console.log("Hi there");
	var input = document.getElementById("file");
	console.log(input.value);

	var file = input.files[0];
	if (!file) {
		return;
	}
	var reader = new FileReader();
	reader.onload = function(e) {
		var file_data = e.target.result;
	    // Display file content
	    console.log(file_data);
	    $.ajax({
	        data : {
	          contents : file_data
	        },
	        type : 'POST',
	        url : '/request'
	    }).done(function(data) {
	        document.getElementById("bob").innerHTML = data;
	    });
	};
	reader.readAsText(file);
	
}
