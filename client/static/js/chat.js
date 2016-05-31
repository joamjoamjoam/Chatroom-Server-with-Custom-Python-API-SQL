	$("#thetext").keyup(function(event){
		if(event.keyCode == 13) {
			$(".chatinputbutton").click();
		}
	});
	
	$(".chatinputbutton").click(function() {
		var usertext = PythonAPI.getUsername() + ": " + $('input[id="thetext"]').val();
		var chatroom = $("#textheader").text();
		var result = PythonAPI.createMessage(usertext, chatroom);
		result = true;
		$('#thetext').val('');
		if(result)
		{
			id = $('.chattext').length + 1;
			if(id % 2 === 0)
			{
				$('.chattext:last').after('<div class="chattext evenbackgroundchat temptext">'+ usertext +'</div>');
			}
			else 
			{
				$('.chattext:last').after('<div class="chattext oddbackgroundchat temptext">'+ usertext +'</div>');
			}
			var element = document.getElementById("textarea");
	    		element.scrollTop = element.scrollHeight;
		}
		else
		{
			alert("Message failed to send.");
		}
			
	});

	$(".roomlist").on('click', '.rButton', function () {
		var id = this.id;
		if(true)
		{
			$("#textheader").text(id);
			$(".temptext").remove();
			var strtext = PythonAPI.chatForName(id);
			var texts = strtext.split('&');  //need to change to w/e delimiter
			for(i = 0; i < texts.length; i++)
			{
				id = $('.chattext').length + 1;
				if(id % 2 === 0)
				{
					$('.chattext:last').after('<div class="chattext evenbackgroundchat temptext">'+ texts[i] +'</div>');
				}
				else
				{
					$('.chattext:last').after('<div class="chattext oddbackgroundchat temptext">'+ texts[i] +'</div>');
				}
			}
			var element = document.getElementById("textarea");
    			element.scrollTop = element.scrollHeight;	
		}
	});

	$(".friendlist").on('click', '.fButton', function () {
		var id = this.id;
	});
	
	$("#showroomwrapper").click(function() {
		var strrooms = PythonAPI.viewChats();
		var rooms = strrooms.split(',');
		for(i = 0; i < rooms.length; i++)
		{
			id = $('.room').length + 1;
			if(id % 2 === 0)
			{
				$('.room:last').after('<div class="room evenbackgroundside temprm" id="room"' + rooms[i] + '">' + rooms[i] + '<button type="button" class="btn btn-primary rButton" id="' + rooms[i] + '">Enter</button></div>');
			}
			else
			{
				$('.room:last').after('<div class="room oddbackgroundside temprm" id="room' + rooms[i] + '">' + rooms[i] + '<button type="button" class="btn btn-primary rButton" id="' + rooms[i] + '">Enter</button></div>');
			}
		}
		$(".tempcontact").remove();
		$("#roomtab").css({"background-color":"#0059b3"});
		$("#contacttab").css({"background-color":"#0066cc"});
		$("#room-wrapper").css({"display":"block"});
		$("#contacts-wrapper").css({"display":"none"});
	});

	$("#showcontactwrapper").click(function() {
		var strfriends = PythonAPI.viewFriendsList();
		var friends = strfriends.split(',');
		for(i = 0; i < friends.length; i++)
		{
			id = $('.thefriend').length + 1;
			if(id % 2 === 0)
			{
				$('.thefriend:last').after('<div class="thefriend contact evenbackgroundside tempcontact" id="friend' + friends[i] + '">' + friends[i] + '<button type="button" class="btn btn-primary fButton" id="' + friends[i] + '">Whatever</button></div>');
			}
			else
			{
				$('.thefriend:last').after('<div class="thefriend contact oddbackgroundside tempcontact" id="friend' + friends[i] + '">' + friends[i] + '<button type="button" class="btn btn-primary fButton" id="' + friends[i] + '">Whatever</button></div>');
			}
		}
		$(".temprm").remove();
		$("#contacttab").css({"background-color":"#0059b3"});
		$("#roomtab").css({"background-color":"#0066cc"});
		$("#contacts-wrapper").css({"display":"block"});
		$("#room-wrapper").css({"display":"none"});
	});
	
	$("#createRoom").click(function() {
		var roomName = $('input[id="room-name"]').val();
		var result = PythonAPI.createChat(roomName);
		if(result) {
			$("#roomModal").modal('hide');
		}
		else {
			$(".roommodalerror").text("Room Creation Failed.");
		}
	});

	$("#joinRoom").click(function() {
		var roomName = $('input[id="room-name"]').val();
		var result = PythonAPI.joinChat(roomName);
		if(result) {
			id = $('.room').length + 1;
			if(id % 2 === 0)
			{
				$('.room:last').after('<div class="room evenbackgroundside temprm" id="room"' + roomName + '">' + roomName + '<button type="button" class="btn btn-primary rButton" id="' + roomName + '">Join</button></div>');
			}
			else
			{
				$('.room:last').after('<div class="room oddbackgroundside temprm" id="room' + roomName + '">' + roomName + '<button type="button" class="btn btn-primary rButton" id="' + roomName + '">Join</button></div>');
			}
			$("#roomModal").modal('hide');
		}
		else{
			$(".roommodalerror").text("Room Join Failed.");
		}
	});	

	$("#createFriend").click(function() {
		var friendName = $('input[id="contact-name"]').val();
		var result = PythonAPI.addUserToFriendsList(friendName);
		if(result) {
			id = $('.thefriend').length + 1;
			if(id % 2 === 0)
			{
				$('.thefriend:last').after('<div class="thefriend contact evenbackgroundside tempcontact" id="friend' + friendName + '">' + friendName + '<button type="button" class="btn btn-primary fButton" id="' + friendName + '">Whatever</button></div>');
			}
			else
			{
				$('.thefriend:last').after('<div class="thefriend contact oddbackgroundside tempcontact" id="friend' + friendName + '">' + friendName + '<button type="button" class="btn btn-primary fButton" id="' + friendName + '">Whatever</button></div>');
			}
			$("#contactModal").modal('hide');
		}
		else {
			$(".contactmodalerror").text("Friend Creation Failed.");
		}
	});

	

	$("#createBlock").click(function() { //not used for now
		var blockName = $('input[id="contact-name"]').val();
		id = $('.theblock').length + 1;
		if(id % 2 === 0) {$('.theblock:last').after('<div class="theblock contact evenbackgroundside">' + blockName + '</div>');}
		else {$('.theblock:last').after('<div class="theblock contact oddbackgroundside">' + blockName + '</div>');}	
	});
	
	$('#roomModal').on('show.bs.modal', function (event) {
	  $(".roommodalerror").text("Looking good!");
	  var button = $(event.relatedTarget); // Button that triggered the modal
	  var modal = $(this);
	  modal.find('.room-modal-title').text('Create/Join Room');
	})

	$('#contactModal').on('show.bs.modal', function (event) {
	  $(".contactmodalerror").text("Looking good!");
	  var button = $(event.relatedTarget); // Button that triggered the modal
	  var modal = $(this);
	  modal.find('.contact-modal-title').text('Add Contact');
	})
	

	
