i = 0;
j = 0;
count = 0;
MM = 0;
SS = 30;
MS = 0;
totle = (MM+1)*60;
d = 180*(MM+1);
MM = "0" + MM;
var gameTime = 30;
var showTime = function(){
    totle = totle - 1;
    if (SS == 0) {
        $(".countBlack").remove();
        $(".pie2").css("-o-transform", "rotate(" + d + "deg)");
        $(".pie2").css("-moz-transform", "rotate(" + d + "deg)");
        $(".pie2").css("-webkit-transform", "rotate(" + d + "deg)");
    } else {
        if (totle > 0 && MS > 0) {
            MS = MS - 1;
            if (MS < 10) {
                MS = "0" + MS
            }
            ;
        }
        ;
        if (MS == 0 && SS > 0) {
            MS = 1;
            SS = SS - 1;
            if (SS < 10) {
                SS = "0" + SS
            }
            ;
        }
        ;
        if (SS == 0 && MM > 0) {
            SS = 30;
            MM = MM - 1;
            if (MM < 10) {
                MM = "0" + MM
            }
            ;
        }
        ;
    }
    ;

    $(".time").html(SS + "<span>秒<br/>之后开始选房</span>");

};

var start1 = function(){
    i = i + 360/((gameTime));
    count = count + 1;
    if(count <= (gameTime/2)+1){
        $(".pie1").css("-o-transform","rotate(" + i + "deg)");
        $(".pie1").css("-moz-transform","rotate(" + i + "deg)");
        $(".pie1").css("-webkit-transform","rotate(" + i + "deg)");
    }else{
        $(".pie2").css("backgroundColor", "#f7592f");
        $(".pie2").css("-o-transform","rotate(" + i + "deg)");
        $(".pie2").css("-moz-transform","rotate(" + i + "deg)");
        $(".pie2").css("-webkit-transform","rotate(" + i + "deg)");
    }
};

var start2 = function(){
    j = j + 1.2;
    count = count + 1;
    if (count == 300) {
        count = 0;
        clearInterval(t2);
        t1 = setInterval("start1()", 100);
    }
    $(".pie2").css("-o-transform","rotate(" + j + "deg)");
    $(".pie2").css("-moz-transform","rotate(" + j + "deg)");
    $(".pie2").css("-webkit-transform","rotate(" + j + "deg)");
};

var countDown = function() {
    i = 0;
    j = 0;
    count = 0;
    MM = 0;
    SS = gameTime+1;
    MS = 0;
    totle = (MM + 1) * gameTime * 10;
    d = 180 * (MM + 1);
    MM = "0" + MM;

    showTime();
    start1();
};
countDown();