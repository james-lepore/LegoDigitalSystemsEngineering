$(document).ready(function() {
    document.getElementById("spinner").style.visibility = "hidden";
	document.getElementById("overlay").style.visibility = "hidden";
});


function getResults() {
	var input = document.getElementById("file");
	var file = input.files[0];
	if (!file){return;}
	if(file["name"].split('.').pop() != "ldr") {
		alert("Invalid File. The file must be an LDraw (.ldr) file.");
		//document.location.reload(true);
		resetPage();
		return;
	}
	document.getElementById("spinner").style.visibility = "visible";
	document.getElementById("overlay").style.visibility = "visible";

	var reader = new FileReader();
	reader.onload = function(e) {
		var file_data = e.target.result;
		//console.log(file_data);
	    $.ajax({
	        data : {
	          contents : file_data
	        },
	        type : 'POST',
	        url : '/request'
	    }).done(function(data) {
	    	if(data[0] == "False"){
	    		document.getElementById("spinner").style.visibility = "hidden";
				document.getElementById("overlay").style.visibility = "hidden";
				resetPage();
	    		alert("Invalid Part Used: " + data[1]);
	    	} else{
	    		fillReqs(file_data, data);
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
		document.getElementById("spinner").style.visibility = "hidden";
		document.getElementById("overlay").style.visibility = "hidden";
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
				if(i > 6){
					results[i].innerHTML = "$" + data[i];
				} else{
					results[i].innerHTML = data[i];
				}
			}
			document.getElementById("spinner").style.visibility = "hidden";
			document.getElementById("overlay").style.visibility = "hidden";
	    });
	}
}


function loadSample(file){
	document.getElementById("spinner").style.visibility = "visible";
	document.getElementById("overlay").style.visibility = "visible";
	document.getElementById("file").value = null;

	$.ajax({
		url:'static/ldr/' + file,
		success:function(file_data){
			$.ajax({
		        data : {
		          contents : file_data
		        },
		        type : 'POST',
		        url : '/request'
		    }).done(function(data) {
		        fillReqs(file_data, data);
		    });
		}
	});
};


function fillReqs(file_data, data){
	var results = document.getElementsByClassName("req");
	for(let i = 0; i < results.length; i++){
		if(data[i]){
			results[i].innerHTML = "✔";
		} else {
			results[i].innerHTML = "❌";
		}
	}

	switch(data[data.length - 1]){
		case "A":
			document.getElementById("chassis_type").innerHTML = "A";
			document.getElementById("chassis_cost").innerHTML = "$30";
			break;
		case "B":
			document.getElementById("chassis_type").innerHTML = "B";
			document.getElementById("chassis_cost").innerHTML = "$40";
			break;
		case "C":
			document.getElementById("chassis_type").innerHTML = "C";
			document.getElementById("chassis_cost").innerHTML = "$50";
			break;
		default:
			document.getElementById("chassis_type").innerHTML = "__";
			document.getElementById("chassis_cost").innerHTML = "__";
	}

	if(data.every(function(k){return k})){
		getMetrics(true, file_data);
	} else{
		getMetrics(false, file_data);
	}
}

function resetPage(){
	document.getElementById("file").value = null;
	var results = document.getElementsByClassName("req");
	for(let i = 0; i < results.length; i++){
		results[i].innerHTML = "❔";
	}
	document.getElementById("chassis_type").innerHTML = "__";
	document.getElementById("chassis_cost").innerHTML = "__";
	var results = document.getElementsByClassName("rsch");
	for(let i = 0; i < results.length; i++){
		results[i].innerHTML = "__";
	}
}