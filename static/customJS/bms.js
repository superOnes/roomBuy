// //ajax提交form表单的方式
// $('#customerOrder').submit(function() {
//    var AjaxURL= "http://10.7.10.198:8000/backstage/createuser/";
//    console.log($('#customerOrder').serialize());
//    $.ajax({
//        type: "POST",
//        dataType: "html",
//        url: AjaxURL + '?Action=' + 'SubmitHandlingFee' + '&OrderNumber=' + $.trim($("#<%=this.txtOrderNumber.ClientID %>").val()),
//        data: $('#customerOrder').serialize(),
//        success: function (data) {
//            var strresult=data;
//            alert(strresult);
//            //加载最大可退金额
//            // $("#spanMaxAmount").html(strresult);
//            return false
//        },
//        error: function(data) {
//            alert("error:"+data.responseText);
//            return false
//        }
//    });
//    return false
// });

// 用户页获取地址
function cityList(provinceId){
 if(!provinceId){
   var urls = "/backstage/getprovince/";
   var appendObj = $("#province");
 }else {
   var urls = "/backstage/getcity/";
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
       appendObj.children(".city").remove();
       for(var i=0; i<data.length; i++){
         appendObj.append("<option class='city' value="+data[i].id+">"+data[i].name+"</option>")
       };
     }else {
       $("#userList tr").remove();
       $(".tip").show();
     }
   },
   error:function(){
     new $.zui.Messager('获取省份、市区数据失败，请检查网络！', {
       placement:'center',
       type: 'danger'
     }).show();
   }
 });
};
// 创建用户获取地址
function createUser(provinceId){
  if(!provinceId){
    var urls = "/backstage/getprovince/";
    var appendObj = $("#provinceC");
  }else {
    var urls = "/backstage/getcity/";
    var appendObj = $("#downtownC");
  }
  $.ajax({
    type:"get",
    url:urls,
    async:true,
    data:{proid:provinceId},
    success:function(results){
      var data = results.data;
      if(results.success){
        appendObj.children(".city").remove();
        for(var i=0; i<data.length; i++){
          appendObj.append("<option class='city' value="+data[i].id+">"+data[i].name+"</option>")
        };
      }
    },
    error:function(){
      new $.zui.Messager('获取省份、市区数据失败，请检查网络！', {
        placement:'center',
        type: 'danger'
      }).show();
    }
  });
};

//获取用户列表数据
function filterUser(province,downtown,value){
 $.ajax({
   type:"get",
   url:"http://10.7.10.198:8000/",
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
};

function deleteUser(id){
  $.ajax({
    type:"post",
    url:"/backstage/delete/",
    async:true,
    data:{id:id},
    success:function(data){
      if(data.success){
        window.location.reload();
      }else{
        new $.zui.Messager(data.msg, {
          placement:'center',
          type: 'danger'
        }).show();
      }
    },
    error:function(){
      alert("删除失败，请检查网络！");
    }
  });
}
