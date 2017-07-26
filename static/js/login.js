
$(function(){

	$(".btnLogin").tap(function(){
		if($(".titleph").val().trim().length==0){
			$(".tips").html("请输入手机号！");
		}
		else if(!telp()){
			$(".tips").html("手机号格式错误！");
		}
		else if($(".titlezj").val().trim().length==0){
			$(".tips").html("请输入证件号！");
		}
		else if(!personId()){
			$(".tips").html("证件号格式错误！");
		}else{
			window.location.href="choiceHouse.html";
		}

	});


	/*订单详情*/
	setInterval(function(){
		var date=new Date();
		var h=date.getHours(),m=date.getMinutes(),s=date.getSeconds();
		$(".order-2").html((h<10?"0"+h:h)+":"+(m<10?"0"+m:m)+":"+(s<10?"0"+s:s));
	},1000);

    $(".houseBtnY").tap(function(){
		$("#houseInfoBlack").show();
	});
	$(".dialog-cancle").tap(function(){
		$("#houseInfoBlack").hide();
	});

	$(".dialog-confirm").tap(function(){
		if(!$(".dialog-check").prop("checked")){
			alert("请同意《活动协议》");
		}else{
			location.href="houseSuccess.html";
		}
	});

// 点击控制样式函数
	$('.choseList p').tap(function () {
		$(this).addClass('choseList-style').siblings().removeClass('choseList-style');
	});

	var aPp=$('.listTileDiv p');
	aPp.each(function(){
		$(this).tap(function(){
			aPp.removeClass('listTile-style');
			$(this).addClass('listTile-style');
		})
	});

	$('.floorList li').tap(function () {
		$(this).addClass('floorList-style').siblings().removeClass('floorList-style');
	});

	/*刷新*/
	$(".fresh").tap(function(){
		location.reload();
	});

	$('.click-down').tap(function () {
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
	$('.click-down-top').tap(function () {
		$(this).addClass('click-down').siblings().removeClass('click-down');
	});

/*在线选房切换*/
	houseTab($(".listTileDiv"),$(".houseTap"));

	houseTab($(".houseUnit"),$(".choseTap"));

	$(".houseUnit p").tap(function(){
		$(this).addClass("listTile-style").siblings().removeClass("listTile-style");
	})

});

function telp (){
	var reg=/^1[3|4|5|7|8]\d{9}$/;
	var hao= $(".titleph").val();
	if(reg.test(hao)){
		return true;
	}else {
		return false;
	}
}

function personId(){
	var reg=/^(\d{15}$|^\d{18}$|^\d{17}(\d|X|x))$/;
	var hao=$(".titlezj").val();
	if(reg.test(hao)){
		return true;
	}else{
		return false;
	}
}

function houseTab(oDiv,aHotab){
	var aP=oDiv.find("p");

	aHotab.hide().eq(1).show();

	aP.each(function(){
		$(this).tap(function(){
			aHotab.hide().eq($(this).index()).show();
		})
	})

}
