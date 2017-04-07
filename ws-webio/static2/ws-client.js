$(document).ready(function(){

        var WEBSOCKET_ROUTE = "/ws";

        if(window.location.protocol == "http:"){
            //localhost
            var ws = new WebSocket("ws://" + window.location.host + WEBSOCKET_ROUTE);
            }
        else if(window.location.protocol == "https:"){
            //Dataplicity
            var ws = new WebSocket("wss://" + window.location.host + WEBSOCKET_ROUTE);
            }
        ws.onopen = function(evt) {
            $("#ws-status").html("Connected");
            };

        ws.onmessage = function(evt) {
	    //alert (evt.data);
	    if(evt.data.includes("user")){
		var msg = new Array();
		msg = evt.data.split(",");
		document.getElementById("mac").value = msg[1] ;
		document.getElementById("name").value = msg[2] ;
		}
	    if(evt.data.includes("[sys]")){
                $("#sys-status").html(evt.data);
		}
	    if(evt.data.includes("update")){
		var msg = new Array();
                msg = evt.data.split(",");
		var x = document.getElementById("remove_list");
		for(i=1;i < msg.length;i++)
		  {
    	            var option = document.createElement("option");
		    option.text = msg[i];
    		    x.add(option);
		  }		
                }

            };

        ws.onclose = function(evt) {
            $("#ws-status").html("Disconnected");
            };

        $("#add").click(function(){
           var name = document.getElementById("name").value;
	   ws.send("adduser" + "," + name );
           document.getElementById("remove_list").options.length = 0;

            });

        $("#remove").click(function(){
            ws.send("remove");
            });

        $("#start").click(function(){
            ws.send("start");
            });

        $("#stop").click(function(){
            ws.send("stop");
            });

	$("#updateuser").click(function(){
            document.getElementById("remove_list").options.length = 0;
            ws.send("updateuser");
            });

	$("#removeuser").click(function(){
	    var id = document.getElementById("remove_list");
	    //alert(id.selectedIndex);
	    var re = "removeuser" + "," + id.selectedIndex + "," + id.value;
 	    ws.send(re); 
            document.getElementById("remove_list").options.length = 0;

            });

	

      });
