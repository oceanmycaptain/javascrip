
// 1、默认左侧移动 产品父级ul的left
var oList = document.getElementById('list')
var num = 0 // left值
var speed = 5
var oTimer = null
// 为了产品移动，后面显示区域不落空，复制一份5个产品
oList.innerHTML += oList.innerHTML
// oList.innerHTML = oList.innerHTML + oList.innerHTML
oTimer = setInterval(fnMove, 50)
function fnMove(){
    num -= speed


    if(num < -1000)
    {
        num = 0
    }

    if(num>0)
    {
        num=-1000
    }

    oList.style.left = num + 'px'
}

// 2、左右箭头单击，改变运动方向
var oBtn01 = document.getElementById('btn01')
var oBtn02 = document.getElementById('btn02')
oBtn02.onclick = function(){
    speed = -5
}
oBtn01.onclick = function(){
    speed = 5
}

// 3、鼠标滑过停止定时器，鼠标离开启动定时器
var oSlide = document.getElementById('slide')
oSlide.onmouseover = function(){
    clearInterval(oTimer)
    oTimer = null
}
oSlide.onmouseout = function(){
    oTimer = setInterval(fnMove, 50)
    // 定时器累加  setInterval(fnMove, 50)
}
