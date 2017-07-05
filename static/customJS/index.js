
$(document).ready(function(){
//	中间部分的高度自适应
	var wrapHeight = $(window).height()-100 ;
	$("#login-wrap").height(wrapHeight);
	$(window).resize(function(){
		var wrapHeight = $(window).height()-100 ;
		$("#login-wrap").height(wrapHeight);
	});
	
})
