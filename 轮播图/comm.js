function $(id){
    return document.getElementById(id);
}


function animate(obj,target){
    clearInterval(obj.timerId);
    obj.timerId =   setInterval(function(){
        //获取当前元素的offsetLeft属性值
        var current = obj.offsetLeft;
        //设置步长值 
        var step = 10;
        step = current < target ? step : -step;
        current += step;
        //将其设置到
        if(Math.abs(target - current) > Math.abs(step)){
            
            obj.style.left = current+"px";
        }else {
            //清除定时器
            clearInterval(obj.timerId);
            obj.style.left = target+"px";
        }
        
    },15);
}