/**
 * Created by pala on 2017/9/21.
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

api.login = function (data, response) {
    var url = '/wap/login.html';
    api.post(url, data, response)
};

api.register = function (data, response) {
    var url = '/wap/register.html';
    api.post(url, data, response)
};

api.findpass = function (data, response) {
    var url = '/wap/findpass.html';
    api.post(url, data, response)
};

api.switchProduct = function (data, response) {
    var url = '/wap/switch_product.html';
    api.post(url, data, response)
};
api.switchCity = function (data, response) {
    var url = '/wap/switch_city.html';
    api.post(url, data, response)
};

api.bugPackage = function (data, response) {
    var url = '/wap/buy_pacakage.html';
    api.post(url, data, response)
};
api.bugProduct = function (data, response) {
    var url = '/wap/buy_product.html';
    api.post(url, data, response)
};
api.numOfProduct = function (data, response) {
    var url = '/wap/numofproduct.html';
    api.post(url, data, response)
};
api.delProduct = function (url, response) {
    api.ajax(url, 'get', {}, response)
};
api.bug = function (data, response) {
    var url = '/wap/buy.html';
    api.post(url, data, response)
};
api.pay = function (data, response) {
    var url = '/wap/payment_method.html';
    api.post(url, data, response)
};
function response(data) {
    if (data.status) {
        window.location.href = data.url
    } else {
        alert(data.message)
    }
}