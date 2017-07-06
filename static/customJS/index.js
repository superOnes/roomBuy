function submitFile(){
	var files = $("#files")[0].files;
    var data = new FormData(); //转化为表单格式的数据
    data.append('f', files[0]);
	$.ajax({
		type:"post",
		url:"http://10.7.10.198:8000/event/import/",
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

function handleBtn(){
	$(".handle-button").click(function(){
		$(this).siblings("div").show();
	})
};
