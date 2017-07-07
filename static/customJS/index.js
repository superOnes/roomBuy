$(document).ready(function(){
//	中间部分的高度自适应
	var wrapHeight = $(window).height()-100 ;
	$("#login-wrap").height(wrapHeight);
	$(window).resize(function(){
		var wrapHeight = $(window).height()-100 ;
		$("#login-wrap").height(wrapHeight);
	});
})

//上传文件
function submitFile(){
	var files = $("#files")[0].files;
    var data = new FormData(); //转化为表单格式的数据
    data.append('f', files[0]);
	$.ajax({
		type:"post",
		url:"../import/",
		async:true,
		data:data,
		cache: false,
        processData: false,//发送的数据将被转换为对象，false就是不转化，默认为true
        contentType: false,
		success:function(){
			window.location.reload();
		},
		error:function(){
			alert("未知错误")
		}
	});
};
