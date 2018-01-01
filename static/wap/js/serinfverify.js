$(function () {
    bindClickBuyProduct();
    bindCalcPrice();
    calcPrice();
});
var csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val();
function bindClickBuyProduct() {
    $('#bugProduct').click(function () {
        calcPrice()
        var ele = $('.weui-bar__item--on');
        var li = [];
        for (var i = 0; i < ele.length; i++) {
            var nid = ele.eq(i).attr('nid');
            var price = ele.eq(i).attr('price');
            if (nid && price) {
                li.push({'nid': nid, 'price': price})
            }
        }
        var product_id = $('#nid').val();
        var price = $('price').val();
        li.push({'nid': product_id, 'price': price});
        var data = {
            'csrfmiddlewaretoken': csrfmiddlewaretoken,
            'nid': JSON.stringify(li)
        };

        api.bugProduct(data, response)
    })
}
// 定时计算产品总价
function bindCalcPrice() {
    setInterval(calcPrice, 2000)
}
// 计算产品总价
function calcPrice() {
    var total_price = 0;
    var prices = $('.weui-tab__bd-item--active');
    for (var i = 0; i < prices.length; i++) {
        var price = prices.eq(i).text().replace('￥', '');
        if (price) {
            total_price += parseFloat(price)
        }
    }
    var price = $('#price').val();
    total_price += parseFloat(price);
    $('#total_price').text(total_price + '元')
}