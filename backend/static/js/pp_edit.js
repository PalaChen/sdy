/**
 * Created by pala on 2017/8/19.
 */

$(function () {
    autoCalcSort();
    packageMinus();
    productMinus();
});

// 点击产品套餐修改按钮
var clickProductBtn = function () {
    $('#product-btn').on('click', function () {
        var nid = $('#product-id').val();
        var data = $('#fm').serialize();
        api.productPackageEdit(nid, data, productResponse)
    })
};

var autoCalcSort = function () {
    var package_info = $('.package-info');
    for (var i = 0; i < package_info.length; i++) {
        package_info.eq(i).children('input[name="sort"]').val(i);
        var product_list = package_info.eq(i).children('.product_list');
        for (var j = 0; j < product_list.length; j++) {
            product_list.eq(j).find("input[name='pp2p_id']").attr('name', `pp2p_id_${i}`);
            product_list.eq(j).find("[name='pp2p_product_id']").attr('name', `pp2p_product_id_${i}`);
            product_list.eq(j).find("input[name='pp2p_price']").attr('name', `pp2p_price_${i}`);
            product_list.eq(j).find("[name='pp2p_description']").attr('name', `pp2p_description_${i}`)
        }
    }
}