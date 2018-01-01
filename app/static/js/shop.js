/**
 * Created by pala on 2017/6/19.
 */

$(function () {
    BindProductTotalPrice();
    BindAddNumber();
    BindReduceNumber();
    BindProductNumber();
    BindHover();
    BindDelete();
    BindTotalPrice();
    BindBuySub();
    BindClickCoupon();
    CouponLinkage();
    ClickCoupon();

});

coupon_price = 0;

// 计算单个商品总价
function BindProductTotalPrice() {
    var counts = $('.productTotalPrice').length;
    for (var i = 0; i <= counts - 1; i++) {
        var cprice = $('.productCprice').eq(i).html();
        cprice = cprice.substring(0, cprice.length - 1);

        var number = $('.t-productNum').eq(i).val();
        var totalPrice = ( cprice * number).toFixed(2);
        //console.log(cprice, number, totalPrice);
        $('.productTotalPrice').eq(i).text(totalPrice + '元')
    }

}

// 自动计算总价
function BindTotalPrice(product_id, number, commodity_type) {
    var p_sum = 0;
    // 获取每一笔订单小计金额
    $('.productTotalPrice').each(function () {
        var c_price = $(this).parent().prevAll().eq(1).children().text();
        var number = $(this).parent().prev().children().children().eq(1).val();
        c_price = c_price.substring(0, c_price.length - 1);
        p_sum += c_price * number;
    });
    p_sum = p_sum.toFixed(2);
    $('#totalPrice').text(p_sum);
    var p_total = 0;
    p_total = $('#totalPrice').text() * 1 - $('#couponPrice').text();

    $('#totalPayPrice').text(p_total);
    var csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val();
    var data = {
        'nid': product_id,
        'number': number,
        'csrfmiddlewaretoken': csrfmiddlewaretoken,
        'type': commodity_type
    };
    // console.log(data)
    SendAjax(data)

}
// 减少购买数量
function BindReduceNumber() {
    $('.shopp-list').on('click', '.productReduce', function () {
        var has_class = $(this).parent().parent().parent().attr('class');
        var number = $(this).next('.t-productNum').val();
        var product_id = $(this).next('.t-productNum').attr('nid');
        var cprice = $(this).next('.t-productNum').attr('p_price');
        if (number == 1) {
        }
        else {
            number = number * 1 - 1;
            $(this).next('.t-productNum').val(number);
            $(this).parent().parent().next('.shopp-subtotal').children('.productTotalPrice').text((cprice * 1 * number).toFixed(2) + '元');
            if (has_class == 'packageInfo') {
                BindTotalPrice(product_id, number, 1);
                location.href = '/cart.html'

            }
            else {
                BindTotalPrice(product_id, number, 0);
            }

        }
    })
}
// 增加购买数量
function BindAddNumber() {
    $('.shopp-list').on('click', '.productAdd', function () {
        var has_class = $(this).parent().parent().parent().attr('class');
        var number = $(this).prev('.t-productNum').val();

        var product_id = $(this).prev('.t-productNum').attr('nid');
        var cprice = $(this).prev('.t-productNum').attr('p_price');

        number = number * 1 + 1;
        // console.log(number, cprice);

        $(this).prev('.t-productNum').val(number);
        $(this).parent().parent().next('.shopp-subtotal').children('.productTotalPrice').text((cprice * 1 * number).toFixed(2) + '元');
        // console.log((cprice * 1 * number).toFixed(2));
        if (has_class == 'packageInfo') {
            BindTotalPrice(product_id, number, 1);
            location.href = '/cart.html'
        }
        else {
            BindTotalPrice(product_id, number, 0);
        }
    })
}
// 购买数量发生变化计算总价
function BindProductNumber() {
    $('.shopp-list').on('input propertychange', '.t-productNum', function () {
        var number = $(this).val();
        var cprice = $(this).attr('p_price');

        $(this).parent().parent().next('.shopp-subtotal').children('.productTotalPrice').text((cprice * 1 * number).toFixed(2) + '元')
        BindTotalPrice()
    })
}


// 发送最新的购买数量ajax
function SendAjax(data) {
    url = '/cart_number.html';
    $.ajax({
        url: url,
        type: 'POST',
        data: data,
        dataType: "json",
        success: function (arg) {
        }
    })
}

// 购物车删除
function BindDelete() {
    var clickState = 0;
    $('#cartForm').on('click', '.shop_delete', function () {
        if (clickState == 1) {
        }
        else {
            clickState = 1;
            var pid = $(this).attr('pid');
            if (pid) {
                var url = '/cart_del.html?type=0&pid=' + pid;
            }
            else {
                var ppid = $(this).attr('ppid');
                var url = '/cart_del.html?type=1&ppid=' + ppid;
            }

            var ths = this;
            $.ajax({
                url: url,
                type: 'GET',
                success: function (arg) {
                    if (arg['status'] == 200) {
                        location.href = '/cart.html'
                    }
                    else {
                        alert('非法操作,请重新刷新页面')
                    }
                }

            })
            clickState = 0
        }
    })
}

// 发送总价格信息
function BindBuySub() {
    var clickState = 0;
    $('#orderButton').click(function () {
        if (clickState == 1) {
        }
        else {
            clickState = 1;
            var total_price = $('#totalPrice').text().trim();
            var coupon_price = $('#couponPrice').text().trim();
            var pay_price = $('#totalPayPrice').text().trim();
            var csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val();
            data = {
                'total_price': total_price,
                'coupon_price': coupon_price,
                'pay_price': pay_price,
                'csrfmiddlewaretoken': csrfmiddlewaretoken
            };
            url = '/buy_info.html';
            $.ajax({
                url: url,
                type: 'POST',
                data: data,
                dataType: "json",
                success: function (arg) {
                    if (arg['status'] == 200) {
                        location.href = arg['url']
                    }
                    else if (arg['status'] == 501) {
                        location.href = arg['url']
                    }
                    clickState = 0
                }
            })
        }

    });
}

// 如何获取发票tips
var differentindex = '';
function BindHover() {
    $('.invoiceTip').hover(function () {
        openMsg();
    }, function () {
        layer.close(differentindex);
    });
}
function openMsg() {
    differentindex = layer.tips('1、 服务完成后90天内，可联系客服索取发票。', '.invoiceTip', {
        tips: [1, ''],
        time: 4000
    })
}

// 使用优惠卷
function BindClickCoupon() {
    $('#couponTitle').click(function () {
        if ($(this).hasClass('active')) {
            $(this).removeClass('active');
            $('#couponHtml').css('display', 'none');
        }
        else {
            $(this).addClass('active');
            $('#couponHtml').css('display', 'block');
        }
    })
}
// 优惠卷Tab切换
function CouponLinkage() {
    $('#couponHtml ul li').click(function () {
        var i = $(this).index();//下标第一种写法
        //var i = $('tit').index(this);//下标第二种写法
        $(this).addClass('active').siblings().removeClass('active');
        $('#coupon' + i).addClass('active').siblings().removeClass('active');
    });
}

function ClickCoupon() {
    $('#coupon1 input').click(function () {
        var price = parseInt($(this).attr('price'));
        var kind = $(this).attr('kind');
        var coupon_id = $(this).val();
        var csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val();
        var coupon_data = {'nid': coupon_id, 'csrfmiddlewaretoken': csrfmiddlewaretoken, 'price': price};
        if ($(this).is(':checked')) {
            if (kind == 0) {
                coupon_price += price;
                $('#couponPrice').text(coupon_price);
                BindTotalPrice();

                api.couponAdd(coupon_data, CouponCallback)
            }

        }
        else {
            if (kind == 0) {
                coupon_price = coupon_price - price;
                $('#couponPrice').text(coupon_price);
                BindTotalPrice();
                api.couponDel(coupon_data, CouponCallback)

            }

        }

    })

}
function CouponCallback() {

}
