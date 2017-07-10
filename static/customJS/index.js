$(document).ready(function(){
//	中间部分的高度自适应
	var wrapHeight = $(window).height() ;
	$("#login-wrap").height(wrapHeight);
	$(window).resize(function(){
		var wrapHeight = $(window).height() ;
		$("#login-wrap").height(wrapHeight);
	});
})

//上传文件
function submitFile(thisID){
	var files = $("#files")[0].files;
	var data = new FormData(); //转化为表单格式的数据
    data.append('filename', files[0]);
    data.append('id', thisID);
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


//取消发布
function Unpublish(thisID){
	$.ajax({
		type:"POST",
		url:"../pubstatus/",
		async:true,
		data:{id:thisID},
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


//清除公测名单
function deleteOrder(thisID){
	$.ajax({
		type:"delete",
		url:"../delete/",
		async:true,
		data:{id:thisID},
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
