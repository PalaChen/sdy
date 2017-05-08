/**
 * Created by pala on 2017/3/31.
 */

var InterValObj; //timer变量，控制时间
var count = 60; //间隔函数，1秒执行
var curCount;//当前剩余秒数
var clickState = 0;//初始化点击状态

$(function () {
    bindOnlyClick();
    bindOrderProcess();
});

function bindOrderProcess() {
    $('#tb_content').on('click', '.glyphicon-search', function () {
        clickState = 1;
        id = $(this).parent().parent().attr('for');
        console.log(id);
        url = '/user/order_process/' + id + '.html';
        setTimeout(Send_Ajax_Order_Process(url), 5000);
    })
}
function Send_Ajax_Order_Process(url) {
    $.ajax({
        url: url,
        type: 'GET',
        success: function (arg) {
            if (arg['status']) {
                console.log(arg['data']);
                $('#orderlist-check-processlist').empty();
                for (var i = 0; i < arg['data'].length; i++) {
                    var li_ele = document.createElement('li');
                    li_ele.setAttribute('class', 'posr clearfix select');
                    var span_ele = document.createElement('span');
                    span_ele.setAttribute('class', 'pull-left_1');
                    var var_ele = document.createElement('var');
                    var_ele.setAttribute('class', 'pull-right_1');
                    span_ele.innerHTML = arg['data'][i]['date'];
                    var_ele.innerHTML = arg['data'][i]['step_name'];
                    li_ele.append(span_ele);
                    li_ele.append(var_ele);
                    $('#orderlist-check-processlist').append(li_ele)
                }
                $('#Model_process').modal('show')
            }
            else {
                alert(arg['message'])
            }
            clickState = 0
        }
    })
}

function bindOnlyClick() {
    $('#user_getcode').click(function () {
        if (clickState == 1) {
        }
        else {
            clickState = 1;
            var url = "user/get_verify_code.html";
            var send_type = $(this).attr('for');
            if (send_type == 'register') {
                var phone = $('input[name="phone"]').val();
                var url = "user/get_verify_code.html?" + "phone=" + phone;
            }


            if (phone) {
                setTimeout(Send_Ajax_VerifyCode(url, this), 60000);
            }
            else {
                if (send_type == 'register') {
                    var parent_ele = $('input[name="phone"]').parent().parent();
                    var div_ele = document.createElement('div');
                    div_ele.setAttribute('class', 'register-li-1 tishi-div-3');
                    div_ele.textContent = '请输入手机号码';
                    parent_ele.append(div_ele);
                }

            }

        }
    });
    $('#submitButton').click(function () {
        if (clickState == 1) {
        } else {
            clickState == 1
            url = '/user/info.html';
            data = $('#userinfoForm');
            setTimeout(Send_Ajax_Edit_Info(url, data), 5000);

        }
    });
    $('#submitMobileButton').click(function () {
        if (clickState == 1) {
        } else {
            clickState == 1
            url = 'user/change_phone.html';
            data = $('#mobileForm');
            setTimeout(Send_Ajax_Edit_Info(url, data), 5000);
        }
    });
    $('#passwordButton').click(function () {
        if (clickState == 1) {                //如果状态为1就什么都不做
        } else {
            clickState = 1;  //如果状态不是1  则添加状态 1
            url = 'user/change_pwd.html';
            data = $('#mobileForm');
            setTimeout(Send_Ajax_Edit_Info(url, data), 5000);

        }
    });

}

function Send_Ajax_Edit_Info(url, data) {
    console.log(data.serialize());
    $.ajax({
        url: url,
        type: 'POST',
        data: data.serialize(),
        success: function (arg) {
            if (arg['status']) {
                $('#Model_result .modal-body').empty();
                $('#Model_result .modal-body').append('<div>' + arg['message'] + '</div>');
                $('#Model_result').modal('show')
            }
            else {
                $('#Model_result .modal-body').empty();
                if (arg['message']) {
                    $('#Model_result .modal-body').append('<div>' + arg['message'] + '</div>');
                }
                else {
                    $('#Model_result .modal-body').append('<div>非法操作，修改失败</div>');
                }
                $('#Model_result').modal('show')
            }
            clickState = 0;
        }
    })
}

function Send_Ajax_VerifyCode(url, ths) {
    $.ajax({
        url: url,
        type: 'GET',
        success: function (arg) {
            if (arg) {
                $(ths).parent().append('<span class="verCodePrompt">已发送，1分钟后可重新获取。</span>')
                curCount = count;
                $("#user_getcode").text(curCount + "秒后重发");
                InterValObj = window.setInterval(SetRemainTime, 1000);
            }
            clickState = 0
        }
    });

}

// 验证码60秒倒计时
function SetRemainTime() {
    if (curCount == 0) {
        window.clearInterval(InterValObj);//停止计时器
        $("#user_getcode").text("重新发送");
        $('.verCodePrompt').remove();
    }
    else {
        curCount--;
        console.log(curCount);
        $("#user_getcode").text(curCount + "秒后重发");
    }
}