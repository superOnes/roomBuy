window.onload = function() {
	var oForm = document.getElementById('loginForm');
	var oUser = document.getElementById('user');
	var oPswd = document.getElementById('pswd');
	var oRemember = document.getElementById('remember');
	//页面初始化时，如果帐号密码cookie存在则填充
	if(getCookie('user') && getCookie('pswd')) {
		oUser.value = getCookie('user');
		oPswd.value = getCookie('pswd');
		oRemember.checked = true;
	};
	//复选框勾选状态发生改变时，如果未勾选则清除cookie
	$("#remember").change(function() {
		if(!this.checked) {
			delCookie('user');
			delCookie('pswd');
		}
	});
	//表单提交事件触发时，如果复选框是勾选状态则保存cookie
	$("#loginForm").submit(function() {
		if(remember.checked) {
			setCookie('user', oUser.value, 7); //保存帐号到cookie，有效期7天
			setCookie('pswd', oPswd.value, 7); //保存密码到cookie，有效期7天
		}
	});
};
//设置cookie
function setCookie(name, value, day) {
	var date = new Date();
	date.setDate(date.getDate() + day);
	document.cookie = name + '=' + value + ';expires=' + date;
};
//获取cookie
function getCookie(name) {
	var reg = RegExp(name + '=([^;]+)');
	var arr = document.cookie.match(reg);
	if(arr) {
		return arr[1];
	} else {
		return '';
	}
};
//删除cookie
function delCookie(name) {
	setCookie(name, null, -1);
};