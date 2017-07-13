
//清除公测名单
function deleteOrder(thisID,url){
	$.ajax({
		type:"POST",
		url:url,
		async:true,
		data:{id:thisID},
		cache: false,
        processData: false,//发送的数据将被序列化，false就是序列化数据，默认为true
        contentType: false,
		success:function(){
			window.location.reload();
		},
		error:function(){
			alert("未知错误")
		}
	});
};
