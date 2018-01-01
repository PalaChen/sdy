/**
 * Created by pala on 2017/7/26.
 */

$(function () {
    getProduct2cityInfo();
    bindOnlyClick();
    bindCategoryShow();
    bugProduct();
});

//获取产品对应的城市信息
var getProduct2cityInfo = function () {
    url = window.location.href;
    var num = url.match(/\d+/g).pop();
    $.ajax({
        url: 'product_city.html' + '?nid=' + num,
        type: 'GET',
        success: function (arg) {
            if (arg['status'] == 200) {
                city_dict = arg['message'];
                $('#city').val(city_dict['city'] + '-' + city_dict['area'])
            }
        }
    })
};


// 模态框
var clickState = 1;
function bindOnlyClick() {
    $('#loginButton').click(function () {
        var data = $('#fm_body');
        var url = '/login_ajax.html';
        var modal = 'Modal_Login';
        //console.log(url);
        send_Ajan_Info(url, data, modal)
    });
    $('#user_getcode').click(function () {
        if (clickState == 1) {
        }
        else {
            clickState = 1;
            var phone = $('#Modal_Register input[name="phone"]').val();
            var url = "user/get_verify_code.html?" + "phone=" + phone;
            setTimeout(Send_Ajax_VerifyCode(url, this), 60000);
        }
    });
}
function send_Ajan_Info(url, data, modal) {
    $.ajax({
        url: url,
        type: 'POST',
        data: $(data).serialize(),
        success: function (arg) {
            //console.log(arg);
            if (arg['status']) {
                window.location.reload();
            } else {
                $('.login_error').text(arg['message'])
            }
            clickState = 0;
        }
    });
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

// 产品分类显示和隐藏
function bindCategoryShow() {
    $('dl dt b').click(function () {
        class_value = $(this).attr('class');
        if (class_value == 'active') {
            $(this).removeClass('active');
            $(this).parent().next().removeClass('show')
        }
        else {
            $(this).addClass('active');
            $(this).parent().next().addClass('show')
        }
    })
}

// 获取类型对应的产品信息
function openProduct(ths) {
    nid = $(ths).attr('for');
    $.ajax({
        url: '/get_cat_product.html?nid=' + nid,
        type: 'GET',
        success: function (arg) {
            //console.log(arg['status']);
            if (arg['status'] == 200) {
                //console.log(arg['data']);
                url = '/product/' + arg['data'] + '.html';
                window.location.href = url;
            }
        }
    })
}

// 监控地区被点击时更新产品信息
function MonitorInput(ths) {
    var p_service_id = $('.item-type').find('.active a').attr('for');
    var area = $(ths).attr('data-id');
    $.ajax({
        url: 'get_product.html?nid=' + p_service_id + '&area=' + area,
        type: 'GET',
        success: function (arg) {
            if (arg['status'] == 200) {
                console.log(arg['data']);
                url = '/product/' + arg['data'] + '.html';
                window.location.href = url;
            }
        }
    })
}
var clickState_1 = 0;

// 商品购买
var bugProduct = function () {

    $('#product_bug').on('click', function () {
        if (clickState_1 == 1) {
        }
        else {
            clickState_1 = 1;
            var product_id = $('input[name="product_id"]').val();
            var params = `pid=${product_id}`;
            api.checkPackage(params, buyProductResponse)
        }
    });
};

var buyProductResponse = function (arg) {
    if (arg['status'] == 200) {
            console.log(arg['data'])
            if (arg['data']) {
                $('#iframeid').attr('src', arg['url']);
                $('#Modal_Package').modal('show');
            }
            else {
                window.location.replace(arg['url'])
            }
        }
    else {
        $('#Modal_Login').modal('show');
        clickState_1 = 0
    }
};