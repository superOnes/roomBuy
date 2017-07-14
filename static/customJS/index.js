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



function statisticsData(thisId){
	var $listBuyer = $("#buyer");
	var $listHouse = $("#houseHot");
//	房源数据获取
	$.ajax({
		type:"get",
		data:{id:thisId},
		url:"/event/househeat/",
		async:true,
		dataType:'JSON',
		success:function(results){
			var result =results.data;
			$listHouse.find("tr").remove();
			for (var i=0; i<result.length; i++) {
				result[i].is_sold ? result[i].is_sold="是":result[i].is_sold="否";
				result[i].is_testsold ? result[i].is_testsold="是":result[i].is_testsold="否";
				$listHouse.append("<tr><td>"+i+"</td><td>"+result[i].building+"</td><td>"+result[i].unit+"</td><td>"+result[i].floor+"</td>"+
				"<td>"+result[i].num+"</td><td>"+result[i].is_sold+"</td><td>"+result[i].price+"</td><td>"+result[i].total+"</td><td>"+result[i].room_num+"</td>"+
				"<td>"+result[i].is_testsold+"</td></tr>");
			}
		},
		error:function(){
			alert("房源热度统计错误！！！")
		}
	});
//	购买者数据获取
	$.ajax({
		type:"get",
		data:{id:thisId},
		url:"http://10.7.10.198:8000/event/purcharseheat/",
		async:true,
		dataType:'JSON',
		success:function(results){
			var result =results.data;
			$listBuyer.find("tr").remove();
			for (var i=0; i<result.length; i++) {
				$listHouse.append("<tr><td>"+i+"</td><td>"+result[i].name+"</td><td>"+result[i].mobile+"</td><td>"+result[i].identication+"</td>"+
				"<td>"+result[i].protime+"</td><td>"+result[i].count+"</td><td>"+result[i].heat+"</td><td>"+result[i].testroom+"</td>"+
				"<td>"+result[i].testtime+"</td><td>"+result[i].openroom+"</td><td>"+result[i].opentime+"</td></tr>")
			}
		},
		error:function(){
			alert("获取购买者热度统计错误！！！")
		}
	});
}
	