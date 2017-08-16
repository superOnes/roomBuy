//ajax提交form表单的方式
$('#customerOrder').submit(function() {
   var AjaxURL= "/backstage/createuser/";
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
           return false
       },
       error: function(data) {
           alert("error:"+data.responseText);
           return false
       }
   });
});


function cityList(provinceId){
 if(!provinceId){
   var urls = "http://10.7.10.198:8000/backstage/getprovince/";
   var appendObj = $("#province");
 }else {
   var urls = "http://10.7.10.198:8000/backstage/getcity/";
   var appendObj = $("#downtown");
 }
 $.ajax({
   type:"get",
   url:urls,
   async:true,
   data:{proid:provinceId},
   success:function(results){
     $(".tip").hide();
     var data = results.data;
     if(results.success){
       appendObj.children("option").remove();
       for(var i=0; i<data.length; i++){
         appendObj.append("<option value="+data[i].id+">"+data[i].name+"</option>")
       };
     }else {
       $("#userList tr").remove();
       $(".tip").show();
     }
   },
   error:function(){
     new $.zui.Messager('获取用户数据失败，请检查网络！', {
       placement:'center',
       type: 'danger'
     }).show();
   }
 });
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
