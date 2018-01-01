/**
 * Created by pala on 2017/6/26.
 */
var api = {};

api.ajax = function (url, method, data, callback) {
    var request = {
        url: url,
        type: method,
        data: data,
        success: function (arg) {
            if (callback != undefined) {
                callback(arg)
            }
        },
        error: function (err) {
            layer.msg('服务器错误')
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


api.couponAdd = function (data, response) {
    url = '/coupon_add.html/';
    api.post(url, data, response)
};
api.couponDel = function (data, response) {
    url = '/coupon_del.html/';
    api.post(url, data, response)
};

api.checkPackage = function (parameter, response) {
    url = `/product/buy.html?${parameter}`;
    api.get(url, response)
};

api.bugPackage = function (data, response) {
    url = '/cart.html';
    api.post(url, data, response)
};
api.wxPay = function (nid, response) {
    url = `/pay/weixin/${nid}.html`;
    api.get(url, response);
};