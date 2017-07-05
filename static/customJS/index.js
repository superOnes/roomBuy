
$(document).ready(function(){
//	中间部分的高度自适应
	var wrapHeight = $(window).height()-100 ;
	$("#login-wrap").height(wrapHeight);
	$(window).resize(function(){
		var wrapHeight = $(window).height()-100 ;
		$("#login-wrap").height(wrapHeight);
	});
	
	
//	表单提交
	$("#loginBtn").click(function(){
		var username = $("#inputText3").val();
		var passwrod = $("#inputPassword3").val();
		$.ajax({
			type:"post",
			url:"../acc/login/",
			async:true,
			data:{username:username ,passwrod:passwrod},
		});
	})
})
