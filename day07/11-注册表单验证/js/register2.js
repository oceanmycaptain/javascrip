$(function(){
    // 表单验证应该失去焦点
    // $('#user_name').blur()
    var $user_name = $('#user_name')
    // oUser_name.onclick = xxx
    // $user_name.click()
    $user_name.blur(function(){
        // 封装函数 调用函数
        fnCheckUser()
    })
    function fnCheckUser(){
        // 获取用户输入的数据
        var vals = $user_name.val()
        // alert(vals)
        // 正则，正则验证用户输入的数据是否合法
        var re = /^\w{6,20}$/

        if(vals == '')
        {
            $user_name.next().show().html('用户名不能为空')
            return
        }
        if(re.test(vals))
        {
            // 合法 -- 隐藏报错信息
            $user_name.next().hide()
        }else{
            // 不合法 -- 报错 -- 下面的span标签显示
            $user_name.next().show().html('用户名是6-20位数字、字母和下划线！')

        }
    }
})