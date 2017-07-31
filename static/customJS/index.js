$(document).ready(function(){
	$("#login-wrap").height($(window).height());
	$(window).resize(function(){
		$("#login-wrap").height($(window).height());
	});
})
//创建活动
$("#createEvent").submit(function(){
    　　if($(".myfileCover").val() == "") {
        　　	new $.zui.Messager('请添加封面', {
        	placement:'center',
		    type: 'important' // 定义颜色主题
		}).show();
	　	return false;
    }else{
    	if($(".myfilePlane_graph").val() == "") {
	        　　	new $.zui.Messager('请添加平面图', {
	        	placement:'center',
			    type: 'important' // 定义颜色主题
			}).show();
	        　	return false;
        }
    }
})


 function checkNumber(value){
 	if(value>0){
	    if(/^[0-9]{11}$/.test(value)){
	       new $.zui.Messager('不可输入特殊字符和“-”', {
	       		placement:'top',
			    type: 'important' // 定义颜色主题
			}).show();
	        return false;
	    }
 	}
}



//上传认筹名单文件
function submitFile(event,thisID){
	alert("正在准备上传，请稍等！");
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
			$(event).attr("disabled","disabled");
			alert("未知错误")
		}
	});
};
//导入房价文件
function roomPriceFile(event,thisID){
	alert("正在上传，请稍等！");
	var files = $("#priceFile")[0].files;
	var data = new FormData(); //转化为表单格式的数据
    data.append('file', files[0]);
    data.append('id', thisID);
	$.ajax({
		type:"POST",
		url:"/import/rooms/",
		async:true,
		data:data,
		cache: false,
        processData: false,//发送的数据将被转换为对象，false就是不转化，默认为true
        contentType: false,
		success:function(data){
			window.location.reload();
		},
		error:function(){
			$(event).attr("disabled","disabled");
			alert("未知错误");
		}
	});
};

//清除公测名单
function deleteOrder(thisId){
	$.ajax({
		type:"POST",
		url:'/acc/ctdelete/',
		async:true,
		data:{id:thisId},
		success:function(){
			new $.zui.Messager('提示消息：成功', {
			    type: 'success' // 定义颜色主题
			}).show("",function(){
				window.location.reload();
			});
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
		url:"/househeat/",
		async:true,
		dataType:'JSON',
		success:function(results){
			var result =results.data;
			$listHouse.find("tr").remove();
			for (var i=0; i<result.length; i++) {
				result[i].is_sold=  result[i].is_sold==true?"是":"否";
				result[i].is_testsold= result[i].is_testsold==true?"是":"否";
				$listHouse.append("<tr><td>"+(i+1)+"</td><td>"+result[i].building+"</td><td>"+result[i].unit+"</td><td>"+result[i].floor+"</td>"+
				"<td>"+result[i].room_num+"</td><td>"+result[i].is_sold+"</td><td>"+result[i].unit_price+"</td><td>"+result[i].area+"</td><td>"+result[i].num+"</td>"+
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
		url:"/purcharseheat/",
		async:true,
		dataType:'JSON',
		success:function(results){
			var result =results.data;
			$listBuyer.find("tr").remove();
			for (var i=0; i<result.length; i++) {
				$listBuyer.append("<tr><td>"+(i+1)+"</td><td>"+result[i].name+"</td><td>"+result[i].mobile+"</td><td>"+result[i].identication+"</td>"+
				"<td>"+result[i].protime+"</td><td>"+result[i].count+"</td><td>"+result[i].heat+"</td><td>"+result[i].testroom+"</td>"+
				"<td>"+result[i].testtime+"</td><td>"+result[i].openroom+"</td><td>"+result[i].opentime+"</td></tr>")
			}
		},
		error:function(){
			alert("获取购买者热度统计错误！！！")
		}
	});
};

//订单下拉框数据显示
function getorderSelect(){
//	活动下拉框列表的显示请求
	$.ajax({
		type:"get",
		url:"/getevent/",
		async:true,
		success:function(results){
			var result =results.data;
			for(var i=0; i<result.length; i++){
				$("#eventList").append("<option value='"+result[i].id+"'>"+result[i].name+"</option>")
			};
			$("#eventList option:first").attr("selected","selected");
		},
		error:function(){
			alert("获取活动列表失败");
		}
	});
}

//订单数据列表显示
function getorderList(thisId,is_test,searchValue){
	var $openList = $("#openList");
	var $exportEach = $("#exportEach");
	$.ajax({
		type:"get",
		data:{id:thisId,is_test:is_test,value:searchValue},
		url:"/orderlist/",
		asunc:true,
		success:function(results){
			$exportEach.attr("href","/exportorder/"+thisId+"&is_test="+is_test+"&value="+searchValue);
			var result =results.data;
			$openList.children("tr").remove();
			for (var i = 0; i < result.length; i++) {
				result[i].status= result[i].status==true ?"已售":"未售";
				$openList.append("<tr><td>"+(i+1)+"</td><td>"+result[i].time+"</td><td>"+result[i].room_num+"</td><td>"+result[i].unit_price+"</td><td>"+result[i].area+"</td><td>"+result[i].realname+"</td>"+
				"<td>"+result[i].mobile+"</td><td>"+result[i].identication+"</td><td>"+result[i].remark+"</td><td>"+result[i].status+"</td></tr>")
			};
		},
		error:function(){
			alert("获取开盘数据失败！！！")
		}
	})
}

//文件图片上传显示
	function getPath(obj,fileQuery,transImg) {
	  var imgSrc = '', imgArr = [], strSrc = '' ;

	  if(window.navigator.userAgent.indexOf("MSIE")>=1){ // IE浏览器判断
	  if(obj.select){
	   obj.select();
	   var path=document.selection.createRange().text;
	   alert(path) ;
	   obj.removeAttribute("src");
	   imgSrc = fileQuery.value ;
	   imgArr = imgSrc.split('.') ;
	   strSrc = imgArr[imgArr.length - 1].toLowerCase() ;
	   if(strSrc.localeCompare('jpg') === 0 || strSrc.localeCompare('jpeg') === 0 || strSrc.localeCompare('gif') === 0 || strSrc.localeCompare('png') === 0){
	   obj.setAttribute("src",transImg);
	   obj.style.filter=
	    "progid:DXImageTransform.Microsoft.AlphaImageLoader(src='"+path+"', sizingMethod='scale');"; // IE通过滤镜的方式实现图片显示
	   }else{
	   //try{
	   throw new Error('File type Error! please image file upload..');
	   //}catch(e){
	   // alert('name: ' + e.name + 'message: ' + e.message) ;
	   //}
	   }
	  }else{
	   // alert(fileQuery.value) ;
	   imgSrc = fileQuery.value ;
	   imgArr = imgSrc.split('.') ;
	   strSrc = imgArr[imgArr.length - 1].toLowerCase() ;
	   if(strSrc.localeCompare('jpg') === 0 || strSrc.localeCompare('jpeg') === 0 || strSrc.localeCompare('gif') === 0 || strSrc.localeCompare('png') === 0){
	   obj.src = fileQuery.value ;
	   }else{
	   //try{
	   throw new Error('File type Error! please image file upload..') ;
	   //}catch(e){
	   // alert('name: ' + e.name + 'message: ' + e.message) ;
	   //}
	   }

	  }

	  } else{
	  var file =fileQuery.files[0];
	  var reader = new FileReader();
	  reader.onload = function(e){

	   imgSrc = fileQuery.value ;
	   imgArr = imgSrc.split('.') ;
	   strSrc = imgArr[imgArr.length - 1].toLowerCase() ;
	   if(strSrc.localeCompare('jpg') === 0 || strSrc.localeCompare('jpeg') === 0 || strSrc.localeCompare('gif') === 0 || strSrc.localeCompare('png') === 0){
	   		obj.setAttribute("src", e.target.result) ;
	   }else{
	   //try{
	   throw new Error('File type Error! please image file upload..') ;
	   //}catch(e){
	   // alert('name: ' + e.name + 'message: ' + e.message) ;
	   //}
	   }

	   // alert(e.target.result);
	  }
	  reader.readAsDataURL(file);
	  }
	 };
