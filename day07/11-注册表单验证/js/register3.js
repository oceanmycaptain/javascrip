$(function(){
    var $userName =  $('#user_name')
    $userName.blus(function(){
        var User_name = $(this).val
        if(User_name.length() == 0){
            $(this).next().show().html('用户名不能为空')
            return false
        }
        var re01 = /^\w{6,20}$/
        if(re01.test())
    })
})