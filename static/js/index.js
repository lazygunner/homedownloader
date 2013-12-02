
var removeFirstLink = function()
{
		$(".downloadLinks").first().remove();
		$(".downloadLinks").first().css("color","green");
};

var DownloadStatus = function()
	{
	var that = this;
	var registerError = function(XMLHttpRequest, textStatus, errorThrown)
		{
			$("#button").removeAttr("disabled");
		};
	var registerSuccess = function(data, textStatus, XMLHttpRequest)
		{
		 try
		 		{
		 			if(data == '')
		 				return;
		 			var downloadStatus = JSON.parse(data)
		 			var per = downloadStatus.per;
		 			var speed = downloadStatus.speed;
		 			var eta = downloadStatus.eta;
		 			var stat = downloadStatus.status;
		 			var perString = per + '%';
		 			
		 			$(".bar").css("width", perString);
		 			$("#perCon").text(perString);
		 			$("#speed").text("Speed:" + speed);
		 			$("#eta").text("Remain:" + eta);
		 			if(stat == 'ing'){		 				
						DownloadStatus.buttonDownPress();
						return;
					}
					else if(stat == 'complete'){
						removeFirstLink()
						$(".bar").css("width", "0%");
		 			$("#perCon").text("0%");
						DownloadStatus.buttonDownPress();
						return;
					}
					else if(stat == 'error'){
						removeFirstLink()
						return;
					}
					else if(stat == 'nomore'){
						$(".downloadLinks").first().remove();
						hideProcess();
						return;
					}
		 		}
		 		catch(error)
		 		{
		 			$("#results").append("<li class='error'>Error parsing JSON.</li>");
		 			DownloadStatus.buttonDownPress();
		 		}
		 		$("#button").removeAttr("disabled");
		 	
		};
		
		
	var buttonDownPress = function()
		{
            
			showProgress();
			$.ajax({data:"", dataType:"text", error: registerError, 
				success: registerSuccess, type: "GET",
				url: "/check"});
		};
	
	return {
		buttonDownPress: buttonDownPress
		}
	}();


var Download = function(){
		var that = this;
		var registerError = function(XMLHttpRequset, textStatus, errorThrown)
		{

		};
		var registerSuccess = function(data, rextStatus, XMLHttpRequest)
		{
				data = decodeURIComponent(data);
				if(data.length > 50)
					data = data.substr(0, 47) + '...';
				$("#linkList").append("<li class=\"downloadLinks\">" + data + "</li>");
				DownloadStatus.buttonDownPress();

				return;
		};
		
		var buttonPress = function()
		{
				var downloadLink = {'link':$("#link").val()};
				if(downloadLink.link == ''){
						alert("Empty Link!");
						return;
				}
					
				$("#link").val('');
			
				$.ajax({data:downloadLink, datraType:"text", error: registerError,
						success: registerSuccess, tyep: "POST", url:"/download/"});
		};
		
		return{
			buttonPress : buttonPress
		}
			
	
}();

var hideProcess = function() {
		$('.bar').hide();
		$('.graph').hide();
		$('#speed').hide();
		$('#eta').hide();		  
	
}

var showProgress = function() {
		$(".downloadLinks").first().css("color","green");
		$('.bar').show();
		$('.graph').show();
		$('#speed').show();
		$('#eta').show();
	
}

$(document).ready(function() {

	$("#download").click(Download.buttonPress);
    $("#check").click(DownloadStatus.buttonDownPress);
	if($('.downloadLinks').size() > 0){
		showProgress();
    $(".downloadLinks").each(function(){
    		$(this).text(decodeURIComponent($(this).text()));
        if ($(this).text().length > 50) {
            $(this).text($(this).text().substr(0, 47));
            $(this).append('...');
        }
    });
    DownloadStatus.buttonDownPress();
	}

});
