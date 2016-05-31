$(".login_submit").click(function() {
	var user = $('input[id="login_username"]').val();
	var pass = $('input[id="login_password"]').val();
	var result = PythonAPI.login(user, pass);
	if(result)
	{
		$(".login_error").html("Loging In...");
	}
	else
	{
		$(".login_error").html("Login Failed!");
	}
});

$(".register_submit").click(function() {
	var user = $('input[id="register_username"]').val();
	var pass = $('input[id="register_password"]').val();
	var bio =  $('input[id="register_bio"]').val();
	var result = PythonAPI.register(user, pass, bio);
	if(result)
	{
		$(".register_error").html("Successfully Registered!");
	}
	else
	{
		$(".register_error").html("Registration Failed!");
	}
});

$(".exitbutton").click(function() {
	PythonAPI.disconnect();
});
