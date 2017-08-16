 //ajax提交form表单的方式
$('#customerOrder').submit(function() {
    var AjaxURL= "/backstage/login/";
    console.log($('#customerOrder').serialize());
    $.ajax({
        type: "POST",
        dataType: "html",
        url: AjaxURL + '?Action=' + 'SubmitHandlingFee' + '&OrderNumber=' + $.trim($("#<%=this.txtOrderNumber.ClientID %>").val()),
        data: $('#customerOrder').serialize(),
        success: function (data) {
            var strresult=data;
            alert(strresult);
            //加载最大可退金额
            // $("#spanMaxAmount").html(strresult);
        },
        error: function(data) {
            alert("error:"+data.responseText);
        }
    });
});


function cityList(){
	$.ajax({
		type:"get",
		url:"",
		async:true,
		success:function(data){
			for(var i=0; i<data.length; i++){
				$("#province").append("<option value="+data[i].id+">"+data[i].name+"</option>")
			};
			filterUser($("#province").val(),$("#downtown").val());
		},
		error:function(){
			alert()
		}
	})
}

//获取用户列表数据
function filterUser(province,downtown,value){
	$.ajax({
		type:"get",
		url:"",
		async:true,
		data:{province:province,downtown:downtown,value:value},
		success:function(data){
//			console.log(data);
			if(data.success){
//				$("#userList").remove("tr").append("<tr><td>"+ +"</td><td>"++"</td><td>"++"</td>"
//				+"<td>"+ +"</td><td>"+ +"</td></tr>")
			}else{
				$("#userList").remove("tr");
//				alert("没有符合条件的用户！")
			}
		},
		error:function(){
			alert("获取用户列表失败。")
		}
	});
}
