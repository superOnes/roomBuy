$(document).ready(function(){
	$("#files").val(""); //清空input fiel 火狐中的缓存

	$("#login-wrap").height($(window).height());
	$(window).resize(function(){
		$("#login-wrap").height($(window).height());
	});

	//创建活动
	$("#createEvent").submit(function(){
		var inputPhone = $("input[name='phone_num']").val();
		var	pattern = /[0-9-()（）]{7,15}/;

		if(!pattern.test(inputPhone)){
			new $.zui.Messager('请输入正确的手机号！', {
				placement:'bottom',
				type: 'danger'
			}).show();
　			return false;
		}else if($(".coverImgFile").html() == "") {
			new $.zui.Messager('请添加封面！', {
				placement:'bottom',
				type: 'danger'
			}).show();
　			return false;
		}
	});

	//创建认筹名单
// 	$("#customerOrder").submit(function(){
// 		var inputMobile = $("input[name='mobile']").val();
// 		var inputIdent = $("input[name='identication']").val();
// 		var pattern = /^\d{17}[\d|X]$/;
// 		if(inputMobile.length < 11){
// 			new $.zui.Messager('请输入正确的手机号！', {
// 				placement:'center',
// 				type: 'danger'
// 			}).show();
// 　			return false;
// 		}else if(!pattern.test(inputIdent)){
// 			new $.zui.Messager('请输入正确的身份证号码！', {
// 				placement:'center',
// 				type: 'danger' // 定义颜色主题
// 			}).show();
// 　			return false;
// 		}
// 	});
});



//上传认筹名单文件
function submitFile(event,thisID){
	$(event).attr("disabled","disabled");
	$(".modal-header button").attr("disabled","disabled");
	$(event).siblings("button").attr("disabled","disabled");
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
		success:function(results){
			if(results.response_state == 200){
				new $.zui.Messager('成功导入'+results.data+'个名单', {
		       		placement:'center',
				    type: 'success' // 定义颜色主题
				}).show("",function(){
					setTimeout(function(){
						window.location.href="/"+thisID+"/customs/";
					},1000)
				});
			}else if(results.response_state == 400){
				new $.zui.Messager(results.msg, {
		       		placement:'center',
				    type: 'primary' // 定义颜色主题
				}).show("",function(){
					$(event).removeAttr("disabled","disabled");
					$(".modal-header button").removeAttr("disabled","disabled");
					$(event).siblings("button").removeAttr("disabled","disabled");
				});
			}
		},
		error:function(){
			$(event).attr("disabled","disabled");
			alert("未知错误");
		}
	});
};
//导入房价文件
function roomPriceFile(event,thisID){
	$(event).attr("disabled","disabled");
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
		success:function(results){
			if(results.response_state == 200){
				new $.zui.Messager('成功导入'+results.data+'套房源', {
		       		placement:'center',
				    type: 'success' // 定义颜色主题
				}).show("",function(){
					setTimeout(function(){
						window.location.href="/"+thisID+"/rooms/";
					},500)
				});
			}else if(results.response_state == 400){
				new $.zui.Messager(results.msg, {
		       		placement:'center',
				    type: 'primary' // 定义颜色主题
				}).show("",function(){
					$(event).attr("disabled","disabled");
				});
			}
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
		success:function(data){
			if(data.success) {
				new $.zui.Messager('提示消息：成功', {
					placement:'center',
			    type: 'success' // 定义颜色主题
				}).show("",function(){
					window.location.reload();
				});
			}
		},
		error:function(){
			alert("未知错误");
			$(this).removeAttr("disabled","disabled")
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
			if(results.success){
				$(".tipH").hide();
				$listHouse.find("tr").remove();
				for (var i=0; i<result.length; i++) {
					result[i].is_sold=  result[i].is_sold==true?"是":"否";
					result[i].is_testsold= result[i].is_testsold==true?"是":"否";
					$listHouse.append("<tr><td>"+(i+1)+"</td><td>"+result[i].building+"</td><td>"+result[i].unit+"</td><td>"+result[i].floor+"</td>"+
					"<td>"+result[i].room_num+"</td><td>"+result[i].is_sold+"</td><td>"+result[i].unit_price+"</td><td>"+result[i].area+"</td><td>"+result[i].num+"</td>"+
					"<td>"+result[i].is_testsold+"</td></tr>");
				};
				if(results.has_next) {
					$(".lookMoreHouse").show();
				}else{
					$(".lookMoreHouse").hide();
				}
			}else{
				$(".lookMoreHouse").hide();
				$listHouse.children("tr").remove();
				$(".tipH").show();
			}
		},
		error:function(){
			alert("获取房源热度统计错误！！！")
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
			if(results.success){
				$(".tipB").hide();
				$listBuyer.find("tr").remove();
				for (var i=0; i<result.length; i++) {
					$listBuyer.append("<tr><td>"+(i+1)+"</td><td>"+result[i].name+"</td><td>"+result[i].mobile+"</td><td>"+result[i].identication+"</td>"+
					"<td>"+result[i].consultant+"</td><td>"+result[i].phone+"</td><td>"+result[i].protime+"</td><td>"+result[i].count+"</td><td>"+result[i].testroom+"</td>"+
					"<td>"+result[i].testtime+"</td><td>"+result[i].openroom+"</td><td>"+result[i].opentime+"</td></tr>")
				};
				if(results.has_next) {
					$(".lookMoreBuyer").show();
				}else{
					$(".lookMoreBuyer").hide();
				}
			}else{
				$(".lookMoreBuyer").hide();
				$listBuyer.children("tr").remove();
				$(".tipB").show();
			}
		},
		error:function(){
			alert("获取购买者热度统计错误！！！")
		}
	});
};



//房源查看更多
function lookMoreHouse(page,eventId){
	$.ajax({
		type:'get',
		url:'/househeat/',
		data:{page:page,id:eventId},
		async:true,
		success:function(results){
			if(results.success){
				var result = results.data;
				for (var i=0; i<result.length; i++) {
						result[i].is_sold=  result[i].is_sold==true?"是":"否";
						result[i].is_testsold= result[i].is_testsold==true?"是":"否";
						$("#houseHot").append("<tr><td>"+(i+1+50*(page-1))+"</td><td>"+result[i].building+"</td><td>"+result[i].unit+"</td><td>"+result[i].floor+"</td>"+
						"<td>"+result[i].room_num+"</td><td>"+result[i].is_sold+"</td><td>"+result[i].unit_price+"</td><td>"+result[i].area+"</td><td>"+result[i].num+"</td>"+
						"<td>"+result[i].is_testsold+"</td></tr>");
				};
				if(results.has_next) {
					$(".lookMoreHouse").show();
				}else{
					$(".lookMoreHouse").hide();
				}
			};
		},
		error:function(){
			new $.zui.Messager('获取房源更多数据失败，请检查服务器！', {
				placement:'center',
				type: 'danger' // 定义颜色主题
			}).show();
		}
	})
}
//购房者热度查看更多
function lookMoreBuyer(page,eventId){
	$.ajax({
		type:'get',
		url:'/purcharseheat/',
		data:{page:page,id:eventId},
		async:true,
		success:function(results){
			if(results.success){
				var result = results.data;
				for (var i=0; i<result.length; i++) {
					$("#buyer").append("<tr><td>"+(i+1+50*(page-1))+"</td><td>"+result[i].name+"</td><td>"+result[i].mobile+"</td><td>"+result[i].identication+"</td>"+
					"<td>"+result[i].consultant+"</td><td>"+result[i].phone+"</td><td>"+result[i].protime+"</td><td>"+result[i].count+"</td><td>"+result[i].testroom+"</td>"+
					"<td>"+result[i].testtime+"</td><td>"+result[i].openroom+"</td><td>"+result[i].opentime+"</td></tr>")
				};
				if(results.has_next) {
					$(".lookMoreBuyer").show();
				}else{
					$(".lookMoreBuyer").hide();
				}
			};
		},
		error:function(){
			new $.zui.Messager('获取购房者更多数据失败，请检查服务器！', {
				placement:'center',
				type: 'danger' // 定义颜色主题
			}).show();
		}
	})
}



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
			var eventId = $("#eventList option:first").val();
			getorderList(eventId,0,"")
			return true;
		},
		error:function(){
			alert("获取活动列表失败");
		}
	});
}

//订单数据列表显示
function getorderList(thisId,is_test,searchValue){
	var $openList = $("#openList");
	$.ajax({
		type:"get",
		data:{id:thisId,is_test:is_test,value:searchValue},
		url:"/orderlist/",
		asunc:true,
		success:function(results){
			if(results.success){
				$(".tip").hide();
				// 导出链接添加
				$("#exportEach").attr("href","/exportorder/?id="+thisId+"&is_test="+is_test+"&value="+searchValue);
				var result =results.data;
				$openList.children("tr").remove();
				for (var i = 0; i < result.length; i++) {
					$openList.append("<tr><td>"+(i+1)+"</td><td>"+result[i].time+"</td><td>"+result[i].room_num+"</td><td>"+result[i].unit_price+"元/㎡</td><td>"+result[i].area+"㎡</td><td>"+result[i].realname+"</td>"+
					"<td>"+result[i].mobile+"</td><td>"+result[i].identication+"</td><td>"+result[i].remark+"</td></tr>")
				};
				if(results.has_next) {
					$("#lookMoreOrder").show();
				}else{
					$("#lookMoreOrder").hide();
				}
			}else{
				$("#exportEach").removeAttr("href","");
				$openList.children("tr").remove();
				$(".tip").show();
				$("#lookMoreOrder").hide();
			}
		},
		error:function(){
			alert("获取开盘数据失败！！！")
		}
	})
};

//订单查看更多
function lookMoreOrder(pageOrder,eventId,is_test,searchValue){
	var $openList = $("#openList");
	$.ajax({
		type:'get',
		url:'/orderlist/',
		data:{page:pageOrder,id:eventId,is_test:is_test,value:searchValue},
		async:true,
		success:function(results){
			if(results.success){
				var result = results.data;
				for (var i=0; i<result.length; i++) {
					$openList.append("<tr><td>"+(i+1+50*(pageOrder-1))+"</td><td>"+result[i].time+"</td><td>"+result[i].room_num+"</td><td>"+result[i].unit_price+"元/㎡</td><td>"+result[i].area+"㎡</td><td>"+result[i].realname+"</td>"+
					"<td>"+result[i].mobile+"</td><td>"+result[i].identication+"</td><td>"+result[i].remark+"</td></tr>")
				};
				if(results.has_next) {
					$("#lookMoreOrder").show();
				}else{
					$("#lookMoreOrder").hide();
				}
			};
		},
		error:function(){
			new $.zui.Messager('获取订单数据失败，请检查服务器！', {
				placement:'center',
				type: 'danger' // 定义颜色主题
			}).show();
		}
	})
}


// 批量操作请求
function batch(ids,isStatic){
	if(ids.length == 0){
		new $.zui.Messager('请选择房源', {
			placement:'center',
			type: 'danger' // 定义颜色主题
		}).show('',function(){
			$(".btn").removeAttr("disabled","disabled");
		});
	}else {
		$.ajax({
			type:'post',
			url:'/updownframe/rooms/',
			data:{checklist:ids,state:isStatic},
			asunc:true,
			success:function(){
				new $.zui.Messager('提示消息：成功', {
					placement:'center',
					type: 'success' // 定义颜色主题
				}).show("",function(){
					window.location.reload();
				});
			},
			error:function(){
				new $.zui.Messager('操作失败，请检查网络！', {
					placement:'center',
					type: 'danger' // 定义颜色主题
				}).show('',function(){
					$(".btn").removeAttr("disabled","disabled");
				});
			}
		});
	};
};

	function quit(e){
    $(e).attr("disabled","disabled");
    $.ajax({
      type:"POST",
      url:"/acc/logout/",
      async:true,
      success:function(){
        window.location.href="/acc/login/";
      },
      error:function(){
        alert("退出失败！")
      }
    });
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
