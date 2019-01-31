var oList = document.getElementById('list')
var num = 0 // left值
var speed = 5
var oTimer = null
// 为了产品移动，后面显示区域不落空，复制一份5个产品
oList.innerHTML += oList.innerHTML
// oList.innerHTML = oList.innerHTML + oList.innerHTML
oTimer = setInterval(fnMove, 50)
var length1 = oList.offsetWidth/2
alert(length1)
function fnMove(){
    num -= speed

    if(num<-length1){
        num = 0
    }
    if(num>0){
        num =-length1
    }
    oList.style.left = num +'px'
}

// 2、左右箭头单击，改变运动方向

var obtn1 = document.getElementById('btn01')
var obtn2 = document.getElementById('btn02')


obtn1.onclick = function(){
    speed = 5
}

obtn2.onclick = function(){
    speed = -5
}

// 鼠标悬停

var oStop = document.getElementById('slide')
oStop.onmouseover = function(){
    clearInterval(oTimer)
    oTimer = null
}

oStop.onmouseout = function(){
    oTimer = setInterval(fnMove, 50)
}