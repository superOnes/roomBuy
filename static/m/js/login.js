var id;
var userid;
var http="";//正式
//var http="http://10.7.10.193:8000"; //测试
//var http="http://10.7.1.34";
$(function(){

	$(".btnLogin").click(function(){
		if($(".titleph").val().trim().length==0){
			$(".tips").html("请输入手机号！");
		}
		//else if(!telp()){
		//	$(".tips").html("手机号格式错误！");
		//}
		else if($(".titlezj").val().trim().length==0){
			$(".tips").html("请输入证件号！");
		}
		//else if(!personIds()){
		//	$(".tips").html("证件号格式错误！");
		//}
		else{

			var tel=$(".titleph").val(),personId=$(".titlezj").val();

			$.ajax({
				type:"get",
				url:http+"/app/prodel/",
				data:{
					tel:tel,
					personId:personId
				},
				success:function(data){
					console.log(data);
					if(data.response_state==200){
						prol(data.objects[0]);

						$("#loginBlack").show();
						$(".proCancle").click(function(){
							$("#loginBlack").hide();
						});

						$(".proSure").click(function(){
							$.ajax({
								type:"POST",
								url:http+"/acc/cuslog/",
								data:{
									userid:$(".userid").html()
								},
								dataType:'JSON',
								success: function (data) {
									console.log(data);
									if(data.response_state==200){
										console.log(data);

										window.location.href = "choiceHouse.html?id="+data.id+"&userid="+$(".userid").html();
										//id=data.id;
										//userid=data.userid;
									}else{
										alert(data.msg);
									}
								},
								error:function(){
									alert('页面出错，请重试！');
								}
							});
						})
					}else{
						alert(data.msg);
					}


				},
				error:function(){
					alert("页面出错，请重试");
				}

			});


		}
	});
});

function prol(data){
	$(".prols").empty();
	$(".prols").append($('<h1>'+data.termname+'</h1>'+
						'<p>'+data.term+'</p>'+
						'<p style="display:none" class="userid">'+data.userid+'</p>'
	));
}

/*首页创建元素*/
function creatEle(data){
	var str1=$('<div class="bannerline">' +
					'<div class="swiper-container" style="width:100%;">' +
						'<div class="swiper-wrapper">' +
							'<div class="swiper-slide"><img src="'+http+data.plane_graph+'"/></div>' +
							'<div class="swiper-slide"><img src="'+http+data.plane_graph+'"></div>' +
							'<div class="swiper-slide"><img src="'+http+data.plane_graph+'"/></div>' +
						'</div>' +
						'<div class="swiper-pagination"></div>' +
					'</div>' +
				'</div>'+
				'<div class="houseQui clear"><h1 class="fl">'+data.name+'</h1><p class="quit fr" onclick="quit()">退出</p></div>'+
				'<div class="phone">咨询电话：'+data.phone+'</div>'+
				'<div class="lineBox">'+
					'<div class="floor">' +
						'<div class="remark"><div class="mark"></div><span class="floor1">公测时间</span></div><div class="flr choicSt">公测开始 '+data.test_start+'<br/>公测结束 '+data.test_ent+'</div>' +
					'</div>'+
					'<div class="floor">' +
						'<div class="remark"><div class="mark"></div><span class="floor1">开盘时间</span></div><div class="flr choicSt">开盘开始 '+data.event_start+'<br/>开盘结束 '+data.event_end+'</div>' +
					'</div>'+
					'<div class="floor"><span class="floor2 bder">活动细则</span> <div class="flr hgt">'+data.description+'</div></div>'+
					'<div class="floor"><span class="floor3 bder">活动须知</span><div class="flr hgt">'+data.notice+'</div></div>'+
					'<div class="floor"><span class="floor2 bder">温馨提示</span> <div class="flr hgt">'+data.tip+'</div></div>' +
				'</div>'+
				'<p class="userid1" style="display:none"></p>'+
				'<div class="btnline"><a href="javascript:;" class="btnL">立即进入</a></div>'
	);
	$(".wapline").append(str1);
	var width = $("body").width();
	$(".swiper-container").css({"width":width});
	var swiper = new Swiper('.swiper-container', {
		pagination: '.swiper-pagination',
		freeModeMomentum : true,
		autoplay : 3000,
		autoplayDisableOnInteraction : false
	});
	var dpr = window.devicePixelRatio;

	for(var i = 0 ;i<$(".floor div.hgt").length;i++){
		var index = i;
		var sindex = i+2;
		var height = parseInt($(".floor div.hgt").eq(index).css("height"));
		$(".floor span").eq(sindex).css({"height":(height/(20)+0.85)+"rem","line-height":(height/(20)+0.85)+"rem"})
	}

}

function telp (){
	var reg=/^1[3|4|5|7|8]\d{9}$/;
	var hao= $(".titleph").val();
	if(reg.test(hao)){
		return true;
	}else {
		return false;
	}
}
function quit(){
	$.ajax({
		type:"POST",
		url:http + "/acc/cusout/",
		data:{
			userid:$(".userid1").html()
		},
		success:function(data){
			window.location.href="login.html";
		},
		error:function(data){
			alert("退出出现未知错误！");
		}
	})
}

function personIds(){
	var reg=/^(\d{15}$|^\d{18}$|^\d{17}(\d|X|x))$/;
	var hao=$(".titlezj").val();
	if(reg.test(hao)){
		return true;
	}else{
		return false;
	}
}

/*选房列表*/
function createList(data){
	var str=$('<ul class="houseTitle clear">'+
				'<li>'+
					'<h3>'+data.event_name+'</h3>'+
					'<p>参与人数：<span>'+data.customer_count+'</span></p>'+
				'</li>'+
				'<li class="order">'+
					'<a href="javascript:;" onclick="myOrder()">'+
					'<i></i>'+
					'<p>订单</p>'+
					'</a>'+
				'</li>'+
				'<li class="fresh">'+
					'<a href="javascript:;">'+
					'<i></i>'+
					'<p>刷新</p>'+
					'</a>'+
				'</li>'+
			'</ul>'+
			'<div class="houseList">'+
				'<div class="listTile clear">'+
					'<div class="listTileDiv fl">'+
						'<p onclick="myShare()" class="sharees">'+
						'<i></i>'+
						'我的收藏'+
						'</p>'+
					'</div>'+
					'<label class="click-down fr" name="true"><i></i></label>'+
				'</div>'+
			'</div>'+
			'<ul class="shareCarList houseTap">'+

			'</ul>'+
			'<div class="endTime">'+
				'<i></i>'+
				'<p id="endTimeing"></p>'+
			'</div>'+
			'<p class="idNum" style="display:none;"></p>'+
			'<p class="userid" style="display:none;"></p>'

	);
	$("#houseList").append(str);
	$("title").html(data.event_name);

}
function data3(result){
	var datap=$('<p class="event_start" style="display:none">'+result.event_start+'</p>'+
				'<p class="event_end" style="display:none">'+result.event_end+'</p>'+
			'<p class="test_ent" style="display:none">'+result.test_ent+'</p>'+
			'<p class="test_start" style="display:none">'+result.test_start+'</p>'
	);
	$("#houseList").append(datap);
}
function myOrder() {
	if((new Date($(".event_start").html()).getTime()<new Date().getTime()&&new Date().getTime() < new Date($(".event_end").html()).getTime())||
		(new Date($(".test_start").html()).getTime()<new Date().getTime()&&new Date().getTime() <new Date($(".test_ent").html()).getTime())){
		window.location.href="order.html?id="+$(".idNum").html()+"&userid="+$(".userid").html();
	}else{
			alert("活动尚未开始");
	}


}
function updataTime(data) {
	setInterval(function() {

		var date = new Date().getTime();  //当前时间
		//活动结束时间
		var date1 = new Date(data.event_start).getTime();//开盘
		var date2 = new Date($(".event_end").html()).getTime();//开盘
		var date3 = new Date($(".test_start").html()).getTime();//公测
		var date4 = new Date($(".test_ent").html()).getTime();//公测
		var date5 = date2 - date;  //时间差的毫秒数
		var date6 = date4 - date;
		//计算出相差天数
		if(date<date3){
			$('#endTimeing').html("公测活动未开始");
		}else if(date>date3&&date<date4){
			if (date6 > 0) {
				var dayss = Math.floor(date6 / (24 * 3600 * 1000));
				//计算出小时数
				var leave11 = date5 % (24 * 3600 * 1000);   //计算天数后剩余的毫秒数
				var hourss = Math.floor(leave11 / (3600 * 1000));
				//计算相差分钟数
				var leave22 = leave11 % (3600 * 1000);       //计算小时数后剩余的毫秒数
				var minutess = Math.floor(leave22 / (60 * 1000));
				//计算相差秒数
				var leave33 = leave22 % (60 * 1000);     //计算分钟数后剩余的毫秒数
				var secondss = Math.round(leave33 / 1000);

				$('#endTimeing').html("距公测动结束还有 " + (dayss < 10 ? "0" + dayss : dayss) + "天 " + (hourss < 10 ? "0" + hourss : hourss) + "小时 " + (minutess < 10 ? "0" + minutess : minutess) + " 分钟" + (secondss < 10 ? "0" + secondss : secondss) + " 秒");
			}
		}else if(date>date4&&date<date1){
			$('#endTimeing').html("开盘活动未开始");
		}else if(date>date1&&date<date2){
			if (date5 > 0) {
				var days = Math.floor(date5 / (24 * 3600 * 1000));
				//计算出小时数
				var leave1 = date5 % (24 * 3600 * 1000);   //计算天数后剩余的毫秒数
				var hours = Math.floor(leave1 / (3600 * 1000));
				//计算相差分钟数
				var leave2 = leave1 % (3600 * 1000);       //计算小时数后剩余的毫秒数
				var minutes = Math.floor(leave2 / (60 * 1000));
				//计算相差秒数
				var leave3 = leave2 % (60 * 1000);     //计算分钟数后剩余的毫秒数
				var seconds = Math.round(leave3 / 1000);

				$('#endTimeing').html("距开盘活动结束还有 " + (days < 10 ? "0" + days : days) + "天 " + (hours < 10 ? "0" + hours : hours) + "小时 " + (minutes < 10 ? "0" + minutes : minutes) + " 分钟" + (seconds < 10 ? "0" + seconds : seconds) + " 秒");
			}

		}else {
			$('#endTimeing').html("开盘活动已结束");
		}

	},1000)
}

/*我的收藏*/
function myShare(){
	$(".sharees").addClass("listTile-style");
	$(".shares").removeClass("listTile-style");
	$(".houseUnit").remove();
	$.ajax({
		type:"get",
		url:http+"/app/followlist/",
		data:{
			userid:$(".userid").html()
		},
		success:function(data){
			if(data.response_state==200){
				console.log(data);
				$(".shareCarList").empty();
				for(var i=0;i<data.objects.length;i++){
					$(".shareCarList").append($('<li class="shareCar-list">'+
						'<a class="share-a">'+
							'<p>'+data.objects[i][0].eventdetail+'</p>'+
							'<span>￥'+data.objects[i][0].price+'</span>'+
							'<p style="display:none" class="shareId">'+data.objects[i][0].house+'</p>'+
						'</a>'+
						'</li>'
					))
				}
				$(".shareCar-list").each(function(){
					$(this).click(function(){
						if((new Date($(".event_start").html()).getTime()<new Date().getTime()&&new Date().getTime() < new Date($(".event_end").html()).getTime())||
							(new Date($(".test_start").html()).getTime()<new Date().getTime()&&new Date().getTime() <new Date($(".test_ent").html()).getTime())){
							window.location.href="houseInfo.html?house="+$(this).find(".shareId").html()+"&id="+$(".idNum").html()+"&userid="+$(".userid").html();
						}else{
							alert("活动尚未开始");
						}
					})
				})
			}else{
				alert("页面错误");
			}

		},
		error:function(){
			alert("出错了");
		}
	})
}




function houseList(data){

	for(var i=0;i<data.building.length;i++){
		$(".listTileDiv").append("<p class='shares'>"+data.building[i]+"</p>");
	}

	var aPp=$('.listTileDiv .shares');
	aPp.each(function(){
		$(this).on("click",function(){
			$(".sharees").removeClass("listTile-style");
			$(".shareCarList").empty();
			aPp.removeClass('listTile-style');
			$(this).addClass('listTile-style');
			$.ajax({
				type:"get",
				url:http+"/app/unit/",
				data:{
					building:$(this).text(),
					id:$(".idNum").html(),
					userid:$(".userid").html()
				},
				dataType:'JSON',
				success: function (data) {
					console.log(data);
					$(".houseUnit").remove();
					if(data.objects[0].unit.length>0){
						var unit = $('<div class="houseTap houseUnit">'+
											'<div class="unite clear"></div>'+
									'</div>'
						);
						$(".shareCarList").after(unit);
					}

					for(var i=0;i<data.objects[0].unit.length;i++){

						var units = $('<p>'+data.objects[0].unit[i]+'</p>');
						$(".unite").append(units);

					}
					var aPps = $(".unite").find("p");
					var build;
					for(var i=0;i<$(".shares").length;i++){
						if($(".shares").eq(i).hasClass("listTile-style")){
							build=$(".shares").eq(i).html();
							console.log(build);
						}
					}
					aPps.each(function(){
						$(this).click(function(){
							aPps.removeClass("listTile-style");
							$(this).addClass("listTile-style");
							console.log($(this).html());

							$.ajax({
								type:"get",
								url:http+"/app/houselist/",
								data:{
									building:build,
									unit:$(this).html(),
									id:$(".idNum").html(),
									userid:$(".userid").html()
								},
								success:function(data){
									console.log(data);
									$(".houseChose").remove();
									var romms=$('<div class="houseChose">'+
														'<div class="floorListbox">'+
															'<ul class="floorChose">'+
															'</ul>'+
															'<div class="tab">'+
																'<div class="shouing"><i></i>在售</div>'+
																'<div class="shoued"><i></i>已售</div>'+
															'</div>'+
														'</div>'+
												'</div>');

									$(".unite").after(romms);
									for(var i=0;i<data.objects.length;i++){
										$(".floorChose").append("<li>"+data.objects[i][0].floor_room_num+"</li>");
										if(new Date($(".event_start").html()).getTime()<new Date().getTime()&&new Date().getTime() < new Date($(".event_end").html()).getTime()){
											if(data.objects[i][0].is_sold){
												$(".floorChose li").eq(i).addClass("floorLi-red");
											}
										}
										if(new Date($(".test_start").html()).getTime()<new Date().getTime()&&new Date().getTime() <new Date($(".test_ent").html()).getTime()){
											if(data.objects[i][0].is_testsold){
												$(".floorChose li").eq(i).addClass("floorLi-red");
											}
										}


									}

									if((new Date($(".event_start").html()).getTime()<new Date().getTime()&&new Date().getTime() < new Date($(".event_end").html()).getTime())||
										(new Date($(".test_start").html()).getTime()<new Date().getTime()&&new Date().getTime() <new Date($(".test_ent").html()).getTime())){
										var aLis=$(".floorChose").find("li");
										aLis.each(function(){
											$(this).click(function(){
												var houseID=data.objects[$(this).index()][0].house;
												window.location.href="houseInfo.html?house="+houseID+"&id="+$(".idNum").html()+'&userid='+$(".userid").html();

											})
										})
									}else{
										alert("活动尚未开始");
									}
								},
								error:function(data){
									alert("出错了");
								}
							})
						})
					});

				},
				error:function(data){
					alert("出错了");
				}
			})
		})
	});

	/*刷新*/
	$(".fresh").on("click",function(){
		location.reload();
	});

	$('.click-down').on("click",function () {
		if($(this).attr('name') == 'true'){
			$(this).attr('name','false');
			$(this).addClass('click-down-top');
			$('.listTileDiv').css("height","auto");
		} else{
			$(this).attr('name','true');
			$(this).addClass('click-down').removeClass('click-down-top');
			$('.listTileDiv').css("height","2rem");
		}

	});
	$('.click-down-top').on("click",function () {
		$(this).addClass('click-down').siblings().removeClass('click-down');
	});
}

/*详情信息*/
function houseInfo(data){
	var houseInfo=$('<div class="houseInfotop">'+
				            '<p><span>'+data.floor+'#'+data.looking+'户</span></p>'+
							'<p><img src="'+http+data.pic+'" /></p>'+
							'<h1>'+data.building_unit+'</h1>'+
							'<div class="houseShare clear">'+
								'<span class="fl"><a href="javascript:;" onclick="backList()">返回房间列表</a></span>'+
								'<span class="fl shareBt">收藏</span>'+
							'</div>'+
					'</div>'+
					'<ul class="houseInfoCont">'+
						'<li>单价<br/><span class="shpri">￥'+data.unit_price+'/m²</span></li>'+
						'<li>户型<br/><span>'+data.house_type+'</span></li>'+
						'<li>楼层<br/><span>'+data.floor+'F</span></li>'+
					'</ul>'+
					'<div class="houseInfoOther">'+
						'<p>其他信息</p>'+
						'<ul>'+
							'<li class="clear">'+
								'<span class="fl"><label>建筑面积</label><i>'+data.area+' m²</i></span>'+
							'</li>'+
							'<li class="clear">'+
								'<span class="fl"><label>售价</label><i>￥'+data.total+'</i></span>'+
							'</li>'+
							'<li class="clear">'+
								'<span class="fl"><label>朝向</label><a>朝'+data.looking+'</a></span>'+
							'</li>'+
							'<li class="clear">'+
								'<span class="fl"><label>产权年限</label><a>'+data.term+'</a></span>'+
							'</li>'+
						'</ul>'+
					'</div>'+
					'<p class="houseID" style="display:none"></p>'+
					'<p class="userId" style="display:none"></p>'+
				    '<p class="idd" style="display:none"></p>'
	);
	var infoBlack=$('<div class="windowBlack" id="houseInfoBlack">'+
						'<div class="dialog">'+
							'<div class="dialog-content-1">'+
								'<p>订单确认</p>'+
							'</div>'+
							'<div class="dialog-content-2">'+
								'<span class="location">'+data.event+'</span><br>'+
								'<span>'+data.building_unit+'</span><br>'+
								'<div></div>'+
								'<span class="left pri">单价：</span><span>￥'+data.unit_price+'</span><br>'+
								'<span class="left floor-unit">户型：</span><span>'+data.house_type+'</span><br>'+
								'<span class="left floor-area">建筑面积：</span><span>1㎡</span><br>'+
								'<div></div>'+
								'<span class="left">客户：</span><span>'+data.realname+'</span><br>'+
								'<span class="left">手机号码：</span><span>'+data.mobile+'</span><br>'+
								'<span class="left">证件号码：</span><span>'+data.identication+'</span>'+
							'</div>'+
							'<div class="dialog-content-3">'+
								'<span class="dialog-agree">'+
								'<input type="checkbox" class="dialog-check"/><i></i>'+
								'我已同意并阅读<a href="javascript:;" onclick="proldel()">《活动协议》</a>'+
								'</span>'+
							'</div>'+
							'<div class="dialog-content-4">'+
								'<div class="dialog-cancle">取消</div>'+
								'<div class="dialog-confirm" onclick="confrim()">确认</div>'+
							'</div>'+
						'</div>'+
					'</div>'
	);
	$("#houseInfo").after(infoBlack);
	$("#houseInfo").append(houseInfo);

	if(new Date($(".event_start").html()).getTime()<new Date().getTime()&&new Date().getTime() < new Date($(".event_end").html()).getTime()){
		if(data.is_sold){
			$(".houseInfoOther").after($('<div class="houseBtnN">房间已售</div>'));
		}else{
			$(".houseInfoOther").after($('<div class="houseBtnY" onclick="buyNow()">立即选择</div>'));
		}

	}else if(new Date($(".test_start").html()).getTime()<new Date().getTime()&&new Date().getTime() <new Date($(".test_ent").html()).getTime()){
		if(data.is_testsold){
			$(".houseInfoOther").after($('<div class="houseBtnN">房间已售</div>'));
		}else{
			$(".houseInfoOther").after($('<div class="houseBtnY" onclick="buyNow()">立即选择</div>'));
		}
		console.log(data.is_testsold);

	}else{
		$(".houseInfoOther").after($('<div class="houseBtnN">活动未开始</div>'));
	}



	if(data.is_followed[0]){
		$(".shareBt").unbind("click",shareBtn);
		$(".shareBt").html("已收藏").css({background:"#999",border:"none",color:"#fff"})
	}else{
		$(".shareBt").bind("click",shareBtn);

	}

	$(".dialog-cancle").click(function(){
		$("#houseInfoBlack").hide();
	});

}
function proldel(){
	window.location.href="protocol.html?userid="+$(".userId").html();
}
function data5(result){
	var datap=$('<p class="event_start" style="display:none">'+result.event_start+'</p>'+
		'<p class="event_end" style="display:none">'+result.event_end+'</p>'+
		'<p class="test_ent" style="display:none">'+result.test_ent+'</p>'+
		'<p class="test_start" style="display:none">'+result.test_start+'</p>'
	);
	$("body").append(datap);
}
function buyNow(){
	if((new Date($(".event_start").html()).getTime()<new Date().getTime()&&new Date().getTime() < new Date($(".event_end").html()).getTime())||
		(new Date($(".test_start").html()).getTime()<new Date().getTime()&&new Date().getTime() < new Date($(".test_ent").html()).getTime())){
		$("#houseInfoBlack").show();
	}else{
		alert("活动尚未开始");
	}
}
function confrim(){
	var id=$(".houseID").html();
	var userid=$(".userId").html();
	var idd=$(".idd").html();
	if(!$(".dialog-check").prop("checked")){
		alert("请同意《活动协议》");
	}else{
		if((new Date($(".event_start").html()).getTime()<new Date().getTime()&&new Date().getTime() < new Date($(".event_end").html()).getTime())||
			(new Date($(".test_start").html()).getTime()<new Date().getTime()&&new Date().getTime() < new Date($(".test_ent").html()).getTime())){
			window.location.href = "houseSuccess.html?house="+id+"&userid="+userid+"&id="+idd;
		}else{
			alert("活动尚未开始");
		}
	}
}
Date.prototype.Format = function(fmt)
{ //author: meizz
	var o = {
		"M+" : this.getMonth()+1,                 //月份
		"d+" : this.getDate(),                    //日
		"h+" : this.getHours(),                   //小时
		"m+" : this.getMinutes(),                 //分
		"s+" : this.getSeconds(),                 //秒
		"q+" : Math.floor((this.getMonth()+3)/3), //季度
		"S"  : this.getMilliseconds()             //毫秒
	};
	if(/(y+)/.test(fmt))
		fmt=fmt.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));
	for(var k in o)
		if(new RegExp("("+ k +")").test(fmt))
			fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));
	return fmt;
};
function orderSu(data){
	var sucess=$('<div class="prompt">'+
						'<img src="../images/success.png">'+
						'<div class="prompt-text">'+
							'<span>恭喜您，选择成功</span><br>'+
							'<span>'+data.room_info+'</span>'+
						'</div>'+
						'<div class="prompt-warning">'+
							'<p>请在<span></span>前，到项目现场办理正式手续。逾期未办理，视为放弃资格。</p>'+
						'</div>'+
						'<div class="prompt-btn">'+
							'<a href="javascript:;" onclick="orderInfos()">订单详情</a>'+
						'</div>'+
						'<p class="orderid" style="display:none;">'+data.orderid+'</p>'+
						'<p class="id1" style="display:none"></p>'+
						'<p class="user1" style="display:none"></p>'+
					'</div>'
	);

	$(".success-container").append(sucess);
	var time1=data.limit*3600*1000+new Date(data.ordertime).getTime();
	$(".prompt-warning span").html(new Date(time1).Format("yyyy-MM-dd hh:mm:ss"));

}
function orderInfos(){
	window.location.href="orderinfo.html?orderId="+$(".orderid").html()+"&id="+$(".id1").html()+"&userid="+$(".user1").html();
}

/*订单*/
function order(data){
	for(var i=0;i<data.objects.length;i++){
		$("body").append($('<div class="order-all">' +
								'<div>'+
									'<div class="order-top">'+
										'<a class="order1">'+
											'<span >订单号:</span>&nbsp;<span>'+data.objects[i][0].order_num+'</span>'+
											'<p>'+data.objects[i][0].time+'</p>'+
										'</a>'+
									'</div>'+
									'<div class="order-right"></div>'+
								'</div>'+
								'<div class="order-middle">'+
									'<table>'+
										'<tr>'+
											'<td>楼盘：</td>'+
											'<td>'+data.objects[i][0].event+'</td>'+
										'</tr>'+
										'<tr class="order-table">'+
											'<td>房间：</td>'+
											'<td>'+data.objects[i][0].room_info+'</td>'+
										'</tr>'+
										'<tr>'+
											'<td>单价：</td>'+
											'<td>￥'+data.objects[i][0].unit_price+'/m²</td>'+
										'</tr>'+
									'</table>'+
									'<p class="checkoderBtn">查看订单详情</p>'+
								'</div>'+

								'<p class="oferId" style="display:none">'+data.objects[i][0].orderid+'</p>'+
							'</div>'
		));
	}

}
function data4(result){
	var datap=$('<p class="event_start" style="display:none">'+result.event_start+'</p>'+
		'<p class="event_end" style="display:none">'+result.event_end+'</p>'+
		'<p class="test_ent" style="display:none">'+result.test_ent+'</p>'+
		'<p class="test_start" style="display:none">'+result.test_start+'</p>'
	);
	$("body").append(datap);
}

/*订单详情*/
function checkInfo(data){
	var orderInfo=$('<div class="order-top2">'+
						'<span class="order-1">'+data.eventname+'</span><span class="order-2"></span>'+
						'<p>'+data.room_info+'</p>'+

					'</div>'+
					'<div class="order-a">'+
						'<div class="order-middle2">'+
							'<p>请在<span class="order_time">'+data.limit+'</span>前，到项目现场办理正式手续。预期问办理，视为放弃资格。</p>'+
							'<p style="color:red;margin-top:5px">请截图保存订单，活动结束之后将不能登录。</p>'+
						'</div>'+
						'<div class="order-bottom2">'+
							'<div class="order-bottom-1">'+
								'<table>'+
									'<tr>'+
										'<td>订单号：</td>'+
										'<td>'+data.order_num+'</td>'+
									'</tr>'+
									'<tr>'+
										'<td>选择时间：</td>'+
										'<td>'+data.ordertime+'</td>'+
									'</tr>'+
								'</table>'+
							'</div>'+
							'<div class="order-bottom-2">'+
								'<table>'+
									'<tr>'+
										'<td>户型：</td>'+
										'<td>'+data.houst_type+'</td>'+
									'</tr>'+
									'<tr>'+
										'<td>建筑面积：</td>'+
										'<td>'+data.area+' m²</td>'+
									'</tr>'+
									'<tr>' +
										'<td>价格</td>'+
										'<td>￥'+data.unit_price+'/m²</td>'+
									'</tr>'+
								'</table>'+
							'</div>'+
							'<div class="order-bottom-3">'+
								'<table>'+
									'<tr>'+
										'<td>客户：</td>'+
										'<td>'+data.customer+'</td>'+
									'</tr>'+
									'<tr>'+
										'<td>手机号码：</td>'+
										'<td>'+data.mobile+'</td>'+
									'</tr>'+
									'<tr>'+
										'<td>证件号码：</td>'+
										'<td>'+data.iidentication+'</td>'+
									'</tr>'+
								'</table>'+
							'</div>'+
						'</div>'+
						'<p class="backIndex">返回列表页</p>'+
				'</div>'
	);
	$(".orderInfoBox").append(orderInfo);

	setInterval(function(){
		var date=new Date();
		var h=date.getHours(),m=date.getMinutes(),s=date.getSeconds();
		$(".order-2").html((h<10?"0"+h:h)+":"+(m<10?"0"+m:m)+":"+(s<10?"0"+s:s));
	},1000);

}
