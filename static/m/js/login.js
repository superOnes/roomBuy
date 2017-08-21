var http="";//正式
//var http="http://10.7.10.193:8000"; //测试
//var http="http://10.7.10.36:8000";
$(function(){

	$(".btnlog").click(function(){
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
			var tel=$(".titleph").val(),personId=$(".titlezj").val(),id=$(".loginId").html();
			var $btnlog=$(".btnlog");
            $btnlog.attr("disabled", "disabled");
			$.ajax({
				type:"POST",
				url:http+"/acc/cuslog/",
				data:{
					tel:tel,
					personId:personId,
					id:id
				},
				success:function(data){
                    $btnlog.removeAttr("disabled");
					if(data.response_state==200){

						prol(data.objects[0]);
						$("#loginBlack").show();
					}else{
						alert(data.msg);
					}
				},
				error:function(){
                    $btnlog.removeAttr("disabled");
					alert("页面出错，请重试");
				}

			});
		}
	});
});

function prol(data){
	$(".prols").empty();
	$(".prols").append($('<h1>'+data.termname+'</h1>'+
						'<p>'+data.term+'</p>'
	));
}
window.alert = function(name){
    var iframe = document.createElement("IFRAME");
    iframe.style.display="none";
    iframe.setAttribute("src", 'data:text/plain,');
    document.documentElement.appendChild(iframe);
    window.frames[0].window.alert(name);
    iframe.parentNode.removeChild(iframe);
};

/*首页创建元素*/
function creatEle(data){
	var str1=$('<div class="bannerline">' +
					'<div class="swiper-container" style="width:100%;">' +
						'<div class="swiper-wrapper">' +
						'</div>' +
						'<div class="swiper-pagination"></div>' +
					'</div>' +
				'</div>'+
				'<div class="houseQui clear"><h1 class="fl">'+data.name+'</h1><p class="quit fr"><input type="button" value="退出" class="quitt"/></p></div>'+
				'<div class="phone">咨询电话：'+data.phone+'</div>'+
				'<div class="lineBox">'+
					'<div class="floor">' +
						'<div class="remark"><div class="mark"></div><span class="floor1">公测时间</span></div><div class="flr choicSt">公测开始 '+data.test_start+'<br/>公测结束 '+data.test_ent+'</div>' +
					'</div>'+
					'<div class="floor">' +
						'<div class="remark"><div class="mark"></div><span class="floor1">开盘时间</span></div><div class="flr choicSt">开盘开始 '+data.event_start+'<br/>开盘结束 '+data.event_end+'</div>' +
					'</div>'+
					'<div class="floor"><span class="floor2 bder">活动细则</span> <div class="flr hgt">'+data.description+'</div></div>'+
					'<div class="floor"><span class="floor3 bder">认购须知</span><div class="flr hgt">'+data.notice+'</div></div>'+
					'<div class="floor"><span class="floor2 bder">温馨提示</span> <div class="flr hgt">'+data.tip+'</div></div>' +
				'</div>'+
			     '<p class="ind1" style="display:none"></p>'+
				'<div class="btnline"><a href="javascript:;" class="btnL">立即进入</a></div>'
	);
	$(".wapline").append(str1);
	for(var i=0;i<data.plane_graph.length;i++){
		$(".swiper-wrapper").append($('<div class="swiper-slide"><img src="'+http+data.plane_graph[i]+'"/></div>'));
	}
	
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
			'<div class="endTime">'+
				'<i></i>'+
				'<p id="endTimeing"></p>'+
			'</div>'+
			'<p class="idNum" style="display:none;"></p>'
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
    window.location.href="order.html?id="+$(".idNum").html()
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
			id:$(".idNum").html()
		},
		success:function(data){
			if(data.response_state==200){
				$(".shareCarList").remove();
				if(data.objects.length==0){
					$(".houseList").after('<ul class="shareCarList houseTap">'+
                        							'<div class="noOne"><img src="../images/none.png" /><p>目前您没有任何收藏！</p></div>'+
                        						'</ul>'
						);
				}else{
                    $(".houseList").after('<ul class="shareCarList houseTap"></ul>');
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
				}

				$(".shareCar-list").each(function(){
					$(this).click(function(){
                        window.location.href="houseInfo.html?house="+$(this).find(".shareId").html()+"&id="+$(".idNum").html();
					})
				})
			}else if(data.response_state==401||data.response_state==403){
                alert(data.msg);
                window.location.href="login.html?id="+$(".idNum").html();
            }else if(data.response_state==405){
                alert(data.msg);
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
	if($(".listTileDiv").height()=="42"){
		$(".click-down").hide();
	}else{
		$(".click-down").show();
        $(".listTileDiv").css("height","42");
	}

	aPp.each(function(){
		$(this).on("click",function(){
            $(".shareCarList").remove();
			$(".sharees").removeClass("listTile-style");
			aPp.removeClass('listTile-style');
			$(this).addClass('listTile-style');
			$.ajax({
				type:"get",
				url:http+"/app/unit/",
				data:{
					building:$(this).text(),
					id:$(".idNum").html()
				},
				dataType:'JSON',
				success: function (data) {
					if(data.response_state==200){
					$(".houseUnit").remove();
					if(data.objects[0].unit.length>0){
						var unit = $('<div class="houseTap houseUnit">'+
											'<div class="unite clear"></div>'+
									'</div>'
						);
						$(".houseList").after(unit);
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
						}
					}
					aPps.each(function(){
						$(this).click(function(){
							aPps.removeClass("listTile-style");
							$(this).addClass("listTile-style");
							$.ajax({
								type:"get",
								url:http+"/app/houselist/",
								data:{
									building:build,
									unit:$(this).html(),
									id:$(".idNum").html()
								},
								success:function(data){
                                    if(data.response_state==200){
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
											$(".floorChose").append("<li>"+data.objects[i].floor_room_num+"</li>");
											if(data.objects[i].sold){
												$(".floorChose li").eq(i).addClass("floorLi-red");
											}
										}
										var aLis=$(".floorChose").find("li");

										aLis.each(function(){
											$(this).click(function(){
												var houseID=data.objects[$(this).index()].house;
												window.location.href="houseInfo.html?house="+houseID+"&id="+$(".idNum").html();
											})
										})
                                    }else if(data.response_state==401||data.response_state==403){
                                        alert(data.msg);
                                        window.location.href="login.html?id="+$(".idNum").html();
                                    }else{
                                        alert(data.msg);
									}
								},
								error:function(){
									alert("出错了");
								}
							})
						})
					});
                 }else if(data.response_state==401||data.response_state==403){
                        alert(data.msg);
                        window.location.href="login.html?id="+$(".idNum").html();
                    }else if(data.response_state==405){
                        alert(data.msg);
                    }else{
                        alert(data.msg);
                    }

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
			$('.listTileDiv').css("height","42");
		}

	});
	$('.click-down-top').on("click",function () {
		$(this).addClass('click-down').siblings().removeClass('click-down');
	});
}

/*详情信息*/
function houseInfo(data){
	var houseInfo=$('<div class="houseInfotop">'+
				             '<p><span class="backList"><a href="javascript:;" onclick="backList()">返回列表</a></span></p>'+
							'<p class="infoImg"><img /></p>'+
							'<div class="houseShare clear">'+
        						'<h1 class="fl">'+data.building_unit+'</h1>'+
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
								'<span class="left floor-area">建筑面积：</span><span>'+data.area+'㎡</span><br>'+
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
		if(data.sold){
			$(".houseInfoOther").after($('<div class="houseBtnN">房间已售</div>'));
		}else{
			$(".houseInfoOther").after($('<div class="houseBtnY" onclick="buyNow()">立即选择</div>'));
		}

	$(".shareBt").bind("click",shareBtn);
	/*这里去掉[0]*/
	if(data.is_followed){
		$(".shareBt").html("已收藏").css({background:"#999",border:"none",color:"#fff"})
	}
	if(data.pic==""){
		$(".infoImg").empty();
	}else{
		$(".infoImg img").prop("src",http+data.pic);
        $(".infoImg img").css({width:"200px",height:"150px",margin:"0 auto"});
	}

	$(".dialog-cancle").click(function(){
		$("#houseInfoBlack").hide();
	});

}
function proldel(){
    $.ajax({
        type:"get",
        url:http+"/app/orderpro/",
        data:{
            id:$(".idd").html()
        },
        success:function(data){
            if(data.response_state==200){
                $("body").append($('<div class="prols proNew">'+
                    '<h1>'+data.objects[0].termname+'</h1>'+
                    '<p>'+data.objects[0].term+'</p>'+
                    '<div class="closePro" onclick="closePro()">关闭</div>'+
                    '</div>'
                ));
            }else if(data.response_state==401||data.response_state==403){
                alert(data.msg);
                window.location.href="login.html?id="+$(".idd").html();
            }else if(data.response_state==405){
                alert(data.msg);
            }else{
                alert(data.msg);
            }
        },
        error:function(){
            alert("页面出错，请重试！");
        }
    });

}
function closePro(){
    $(".proNew").remove();
}
function buyNow(){
    $("#houseInfoBlack").show();
}
function confrim(){
	var id=$(".houseID").html();
	var idd=$(".idd").html();
	if(!$(".dialog-check").prop("checked")){
		alert("请同意《活动协议》");
	}else{
        $.ajax({
            type: "get",
            url: http + "/app/captcha/",
            data: {
                id: idd
            },
            success: function (data) {
                console.log(data);
                $("#houseInfoBlack").hide();
                $(".code").remove();
                var code = $('<div class="code">' +
                    '<div class="codebox">' +
                    '<h3>安全验证</h3>' +
                    '<p>安全验证问题：</p>' +
                    '<p class="questi">'+data.formula+'</p>' +
                    '<ul class="codeOption"></ul>' +
                    '<p>请在提交前回答！</p>'+
                    '</div>' +
                    '</div>');
                $("body").append(code);
                for(var i=0;i<data.opt.length;i++){
                	$(".codeOption").append($('<li>'+data.opt[i]+'</li>'));
				}
                $(".codeOption li").each(function(){
                    $(this).click(function(){
                        $(this).css({color:"#f95c30",background:"#fff",border:"none"}).siblings().css({color:"#fff",background:"none",border:"solid 1px #fff"});
                        var capcha=$(this).html();
                        console.log(capcha);
                        $.ajax({
                            type: "POST",
                            url: http + "/app/checkcaptcha/",
                            data: {
                                id: idd,
                                value:capcha
                            },
                            success: function (data) {
                            	console.log(data);
                                if(data.response_state==200){
                                    window.location.href = "houseSuccess.html?house="+id+"&id="+idd;
                                }else if(data.response_state==401||data.response_state==403){
                                    window.location.href="login.html?id="+idd;
                                }else if(data.response_state==412){
                                	alert(data.msg);
								}else if(data.response_state==415){
                                    window.location.href="houseList.html?id="+idd;
								}


                            },
                            error: function () {
                                alert("页面出错，请重试！");
                            }
                        })

                    })
                });

            },
            error: function () {
                alert("页面出错，请重试！");
            }
        })
	}
}
function codeSure(){
	if($(".codeText").val().length!=0){

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
							'<p>请在<span>'+data.limit+'</span>前，到项目现场办理正式手续。逾期未办理，视为放弃资格。</p>'+
						'</div>'+
						'<div class="prompt-btn">'+
							'<a href="javascript:;" onclick="orderInfos()">订单详情</a>'+
						'</div>'+
						'<p class="orderid" style="display:none;">'+data.orderid+'</p>'+
						'<p class="id1" style="display:none"></p>'+
					'</div>'
	);

	$(".success-container").append(sucess);
	if(data.is_test){
		$(".prompt-warning").empty();
	}
}

/*购买失败*/
function buyFailure(data){
	var failure = $('<div class="recommend clear">' +
						'<i></i><p>为您推荐</p><i></i>'+
					'</div>'+
					'<ul class="shareFrom"></ul>'
	);
    $(".success-container").append(failure);
}



function orderInfos(){
	window.location.href="orderinfo.html?orderId="+$(".orderid").html()+"&id="+$(".id1").html();
}
function order(data){
	if(data.objects.length==0){
		$("body").append('<div class="noOne"><img src="../images/none.png" /><p>目前您没有任何订单！</p></div>');
	}else{
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
            if(data.objects[i][0].is_test){
                $(".order-all").eq(i).find(".order-right").append($('<img src="../images/test.png" />'));
            }
		}
	}
}

/*订单详情*/
function checkInfo(data){
	var orderInfo=$('<div class="order-top2">'+
						'<span class="order-1">'+data.eventname+'</span><span class="order-2"></span>'+
						'<p>'+data.room_info+'</p>'+

					'</div>'+
					'<div class="order-a">'+
						'<div class="order-middle2">'+
							'<p>请在<span class="order_time">'+data.limit+'</span>前，到项目现场办理正式手续。逾期未办理，视为放弃资格。</p>'+
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
										'<td>'+data.house_type+'</td>'+//改正拼写
									'</tr>'+
									'<tr>'+
										'<td>建筑面积：</td>'+
										'<td>'+data.area+' m²</td>'+
									'</tr>'+
									'<tr>' +
										'<td>价格:</td>'+
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
										'<td>'+data.identication+'</td>'+
									'</tr>'+
								'</table>'+
							'</div>'+
						'</div>'+
						'<p class="backIndex">返回列表页</p>'+
				'</div>'
	);
	$(".orderInfoBox").append(orderInfo);
    if(data.is_test){
        $(".order-middle2").empty();
        $(".order-bottom-1 table").append($('<tr class="ordertype">'+
            '<td>订单类型：</td>'+
            '<td>公测订单</td>'+
            '</tr>'));
    }else{
        setInterval(function(){
            var dateNew= new Date(data.limit).getTime() - new Date().getTime();
            if(dateNew>0){
                var hours = Math.floor(dateNew / (3600 * 1000));
                //计算相差分钟数
                var leave2 = dateNew % (3600 * 1000);       //计算小时数后剩余的毫秒数
                var minutes = Math.floor(leave2 / (60 * 1000));
                //计算相差秒数
                var leave3 = leave2 % (60 * 1000);     //计算分钟数后剩余的毫秒数
                var seconds = Math.round(leave3 / 1000);


                $('.order-2').html((hours < 10 ? "0" + hours : hours) + "小时 " + (minutes < 10 ? "0" + minutes : minutes) + " 分钟" + (seconds < 10 ? "0" + seconds : seconds) + " 秒");
            }else{
                $('.order-2').html("订单无效");
            }

        },1000);
    }
}
