/**
 * Created by pala on 2017/7/15.
 */
var api = {};

api.ajax = function (url, method, data, callback) {
    var request = {
        url: url,
        type: method,
        data: data,
        success: function (arg) {
            callback(arg)
        },
        error: function (arg) {
            layer.msg('服务器连接失败，请重新再试')
        }
    };
    $.ajax(request)
};

api.get = function (url, response) {
    //log(url);
    api.ajax(url, 'get', {}, response)
};
api.post = function (url, data, response) {
    api.ajax(url, 'post', data, response)
};

api.getAreaProduct = function (parameter, response) {
    url = '/admin/get_area_product.html?' + parameter;
    api.get(url, response)
};

api.productAdd = function (data, response) {
    url = '/admin/product_add.html';
    api.post(url, data, response)
};

api.productEdit = function (nid, data, response) {
    url = `/admin/product_edit/${nid}.html`;
    api.post(url, data, response)
};

api.productPackageEdit = function (nid, data, response) {
    url = `/admin/product_pacakage_edit/${nid}.html`;
    api.post(url, data, response)
};
api.codeStatusEdit = function (data, response) {
    url = `/admin/service/pay_state.html`;
    api.post(url, data, response)
};

api.handselCoupon = function (data, response) {
    url = '/admin/handsel_coupon.html';
    api.post(url, data, response)
};