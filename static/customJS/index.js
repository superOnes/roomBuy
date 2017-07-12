
//上传认筹名单文件
function submitFile(thisID){
	var files = $("#files")[0].files;
	var data = new FormData(); //转化为表单格式的数据
    data.append('filename', files[0]);
    data.append('id', thisID);
	$.ajax({
		type:"POST",
		url:"/acc/import/",
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
//导入房价文件
function roomPriceFile(thisID){
	var files = $("#priceFile")[0].files;
	var data = new FormData(); //转化为表单格式的数据
    data.append('file', files[0]);
    data.append('id', thisID);
	$.ajax({
		type:"POST",
		url:"/event/importprice/",
		async:true,
		data:data,
		cache: false,
        processData: false,//发送的数据将被转换为对象，false就是不转化，默认为true
        contentType: false,
		success:function(){
			window.location.reload();
		},
		error:function(){
			alert("未知错误");
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


//清除公测名单\\\ 删除认筹名单
function deleteOrder(thisID,url){
	$.ajax({
		type:"POST",
		url:url,
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

function onkeypress(event) {
    var x = event.which || event.keyCode;
    
    
}
