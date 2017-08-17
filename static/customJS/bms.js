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
function test(){
  var username = $("input[name='username']").val();
  var name = $("input[name='name']").val();
  var password = $("input[name='password']").val();
  var house_limit = $("input[name='house_limit']").val();
  var province = $("#provinceC").val();
  var downtown = $("#downtownC").val();
  if(username=="" || name=="" || password=="" || house_limit=="" || province==0 || downtown==0){
      new $.zui.Messager("请填写必填项", {
        placement:'center',
        type: 'danger'
      }).show()
  }else{
    var form = new FormData(document.getElementById("customerOrder"));
    $.ajax({
        url:"/backstage/createuser/",
        type:"post",
        data:form,
        processData:false,
        contentType:false,
        success:function(data){
          if(data.success){
            new $.zui.Messager('创建成功！', {
              placement:'center',
              type: 'success'
            }).show("",function(){
              setTimeout(function(){
                window.location.reload();
              },1000)
            });
          }else {
            new $.zui.Messager(data.msg, {
              placement:'center',
              type: 'danger'
            }).show()
          }
        },
        error:function(e){
          new $.zui.Messager("创建失败，请检查网络！", {
            placement:'center',
            type: 'danger'
          }).show()
        }
    });
  }
}


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
  window.location.href="?province="+province+"city="+downtown+"&value="+value;
//  $.ajax({
//    type:"get",
//    url:"http://10.7.10.198:8000/backstage/",
//    async:true,
//    data:{province:province,downtown:downtown,value:value},
//    success:function(data){
// //			console.log(data);
//      if(data.success){
// //				$("#userList").remove("tr").append("<tr><td>"+ +"</td><td>"++"</td><td>"++"</td>"
// //				+"<td>"+ +"</td><td>"+ +"</td></tr>")
//      }else{
//        $("#userList").remove("tr");
// //				alert("没有符合条件的用户！")
//      }
//    },
//    error:function(){
//     //  alert("获取用户列表失败。")
//    }
 // });
};
// 删除用户
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
// 密码重置
function resetUser(id){
  $.ajax({
    type:"put",
    url:"/backstage/reset/",
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
      alert("重置密码失败，请检查网络！");
    }
  });
};
// // 编辑用户
// function editUser(id){
//   $.ajax({
//     type:"post",
//     url:"/backstage/delete/",
//     async:true,
//     data:{id:id},
//     success:function(data){
//       if(data.success){
//         window.location.reload();
//       }else{
//         new $.zui.Messager(data.msg, {
//           placement:'center',
//           type: 'danger'
//         }).show();
//       }
//     },
//     error:function(){
//       alert("保存失败，请检查网络！");
//     }
//   });
// }
