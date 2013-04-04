$(document).ready(function() {
	document.uid = $('#uid').val();
	document.roomname = $('#roomname').val(); 
	
	setTimeout(openconnection, 100);
	var box = null;
	var user = $('#Iam').val();
    var val = "Chat Room";
    box = $("#chat_div").chatbox({id:user, 
                                      user:{key : document.uid},
                                      title : val,
                                      messageSent : function(id, user, msg) {
                                         
                                      }});
   
	});

function openconnection() {
	jQuery.getJSON('/cart/registercallback', {uid: document.uid, roomname : document.roomname },
		function(data, status, xhr) {
		            var roomofsender = data['room'] ;
		            var roomofreceptor = document.roomname ;  
		if (roomofsender == roomofreceptor){
					var msg = data['content'] ;
					var id = data['user'] ;
					$("#chat_div").chatbox("option", "boxManager").addMsg(id, msg);
					setTimeout(openconnection, 0);
					
		}
		else {
			setTimeout(openconnection, 0);
		}
			
		}
	);
}
