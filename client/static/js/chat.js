	$(".chatinputbutton").click(function() {
		//var testing = PythonAPI.testAPI("test1","test2");
		var usertext = $('input[id="thetext"]').val();
		id = $('.chattext').length + 1;
		if(id % 2 === 0) {$('.chattext:last').after('<div class="chattext evenbackgroundchat">'+ usertext +'</div>');}
		else {$('.chattext:last').after('<div class="chattext oddbackgroundchat">'+ usertext +'</div>');}
		var element = document.getElementById("textarea");
    		element.scrollTop = element.scrollHeight;
		
	});

	$("#showroomwrapper").click(function() {
		$("#roomtab").css({"background-color":"#0059b3"});
		$("#contacttab").css({"background-color":"#0066cc"});
		$("#room-wrapper").css({"display":"block"});
		$("#contacts-wrapper").css({"display":"none"});
	});

	$("#showcontactwrapper").click(function() {
		$("#contacttab").css({"background-color":"#0059b3"});
		$("#roomtab").css({"background-color":"#0066cc"});
		$("#contacts-wrapper").css({"display":"block"});
		$("#room-wrapper").css({"display":"none"});
	});
	
	$("#createRoom").click(function() {
		var roomName = $('input[id="room-name"]').val();
		id = $('.room').length + 1;
		if(id % 2 === 0) {$('.room:last').after('<div class="room evenbackgroundside" id="room">' + roomName + '</div>');}
		else {$('.room:last').after('<div class="room oddbackgroundside" id="room">' + roomName + '</div>');}	
	});	

	$("#createFriend").click(function() {
		var friendName = $('input[id="contact-name"]').val();
		id = $('.thefriend').length + 1;
		if(id % 2 === 0) {$('.thefriend:last').after('<div class="thefriend contact evenbackgroundside">' + friendName + '</div>');}
		else {$('.thefriend:last').after('<div class="thefriend contact oddbackgroundside">' + friendName + '</div>');}	
	});

	$("#createBlock").click(function() {
		var blockName = $('input[id="contact-name"]').val();
		id = $('.theblock').length + 1;
		if(id % 2 === 0) {$('.theblock:last').after('<div class="theblock contact evenbackgroundside">' + blockName + '</div>');}
		else {$('.theblock:last').after('<div class="theblock contact oddbackgroundside">' + blockName + '</div>');}	
	});
	
	$('#roomModal').on('show.bs.modal', function (event) {
	  var button = $(event.relatedTarget); // Button that triggered the modal
	  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
	  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
	  var modal = $(this);
	  modal.find('.room-modal-title').text('Add or Create Room');
	})

	$('#contactModal').on('show.bs.modal', function (event) {
	  var button = $(event.relatedTarget); // Button that triggered the modal
	  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
	  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
	  var modal = $(this);
	  modal.find('.contact-modal-title').text('Add or Block Contact');
	})


/*code by Pavel Komiagin*/
(function () {
    var Message;
    Message = function (arg) {
        this.text = arg.text, this.message_side = arg.message_side;
        this.draw = function (_this) {
            return function () {
                var $message;
                $message = $($('.message_template').clone().html());
                $message.addClass(_this.message_side).find('.text').html(_this.text);
                $('.messages').append($message);
                return setTimeout(function () {
                    return $message.addClass('appeared');
                }, 0);
            };
        }(this);
        return this;
    };
    $(function () {
        var getMessageText, message_side, sendMessage;
        message_side = 'right';
        getMessageText = function () {
            var $message_input;
            $message_input = $('.message_input');
            return $message_input.val();
        };
        sendMessage = function (text) {
            var $messages, message;
            if (text.trim() === '') {
                return;
            }
            $('.message_input').val('');
            $messages = $('.messages');
			/* Currently set to send messages back-to-back between self */
            message_side = message_side === 'left' ? 'right' : 'left';
            message = new Message({
                text: text,
                message_side: message_side
            });
            message.draw();
            return $messages.animate({ scrollTop: $messages.prop('scrollHeight') }, 300);
        };
        $('.send_message').click(function (e) {
            return sendMessage(getMessageText());
        });
        $('.message_input').keyup(function (e) {
            if (e.which === 13) {
                return sendMessage(getMessageText());
            }
        });
    });
}.call(this));
