function getResults() {
	var input = document.getElementById("file");
	var file = input.files[0];
	if (!file){return;}
	if(file["name"].split('.').pop() != "ldr") {
		alert("Invalid File");
		var results = document.getElementsByClassName("req");
		for(let i = 0; i < results.length; i++){
			results[i].innerHTML = "❔";
		}
		var results = document.getElementsByClassName("rsch");
		for(let i = 0; i < results.length; i++){
			results[i].innerHTML = "__";
		}
		return;
	}
	var reader = new FileReader();
	reader.onload = function(e) {
		var file_data = e.target.result;
	    $.ajax({
	        data : {
	          contents : file_data
	        },
	        type : 'POST',
	        url : '/request'
	    }).done(function(data) {
	        var results = document.getElementsByClassName("req");
			for(let i = 0; i < results.length; i++){
				if(data[i]){
					results[i].innerHTML = "✔";
				} else {
					results[i].innerHTML = "❌";
				}
			}

			if(data.every(function(k){return k})){
				getMetrics(true, file_data);
			} else{
				getMetrics(false, file_data);
			}
	    });
	};
	reader.readAsText(file);
}


function getMetrics(reqMet, parts_list){
	if(!reqMet){
		var results = document.getElementsByClassName("rsch");
		for(let i = 0; i < results.length; i++){
			results[i].innerHTML = "__";
		}
	} else{
		$.ajax({
	        data : {
	          contents : parts_list
	        },
	        type : 'POST',
	        url : '/metrics'
	    }).done(function(data) {
	       var results = document.getElementsByClassName("rsch");
		    for(let i = 0; i < results.length; i++){
				results[i].innerHTML = data[i];
			}

	    });
	}
}

