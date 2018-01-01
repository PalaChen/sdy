/**
 * Created by pala on 2017/7/12.
 */
$(function () {
    // packagePlus();
    // productPlus();
    productTab();
    clickNoBugOption();
    clickProductBtn();
    initKindEditor();
});

var sort = 0;

function packagePlus(that) {
    var clone_obj = $(that).parent().parent().clone();
    sort += 1;
    clone_obj.find('input[name="sort"]').val(sort);
    clone_obj.find('select[name^= "pp2p_product_id_"]').attr('name', "pp2p_product_id_" + sort);
    clone_obj.find('input[name^= "pp2p_product_id_"]').attr('name', "pp2p_product_id_" + sort);
    clone_obj.find('input[name^= "pp2p_price_"]').attr('name', "pp2p_price_" + sort);
    clone_obj.find('textarea[name^= "pp2p_description_"]').attr('name', "pp2p_description_" + sort);
    $('#advancedSettings').append(clone_obj);
    packageMinus();
    productMinus();
    clickNoBugOption();
}

var packageMinus = function () {
    $('.package-minus').on('click', function () {
        $(this).parent().parent().remove();
    })
};

function productPlus(that) {
    var clone_obj = $(that).parent().parent().clone();
    $(that).parent().parent().parent().append(clone_obj);
    productMinus();
    clickNoBugOption();
}

var productMinus = function () {
    $('.product-minus').on('click', function () {
        $(this).parent().parent().remove();
    })
};

// 产品信息tab切换
var productTab = function () {
    $('#title_tab a').on('click', function () {
        var i = $(this).index();
        if (i == 0) {
            $('#upload_image').show();
            tabInfo(this, i)
        } else if (i == 2) {
            var that = this;
            layer.confirm('产品信息和产品描述是否填写完成', {
                btn: ['已填写', '还没填'] //按钮
            }, function (index) {
                layer.close(index);
                $('#upload_image').hide();
                tabInfo(that, i);
                // console.log(222)
                var code = $('select[name="area"]').val();
                var parameter = 'code=' + code;
                api.getAreaProduct(parameter, responseProductAdd)
            }, function (index) {
                layer.close(index);
            });
        }
        else {
            $('#upload_image').hide();
            tabInfo(this, i)
        }

    })
};

var tabInfo = function (that, i) {
    $(that).addClass('btn-primary').siblings().removeClass('btn-primary');
    $('#ProductInfo .basicInfo').eq(i).show().siblings().hide();
};

var responseProductAdd = function (arg) {
    if (arg.status = 200) {
        $('select[name^= "pp2p_product_id_0"]').html('');
        var options_ele = '<option value="">---------------</option>';
        for (var i = 0; i < arg.message.length; i++) {
            var option_ele = `<option value="${arg.message[i].id}">${arg.message[i].p_name}</option>`;
            options_ele += option_ele
        }
        options_ele += '<option value="noBuy" class="noBuyOption">不购买该产品</option>';
        $('select[name^= "pp2p_product_id_0"]').append(options_ele)
    } else {
        layer.msg('请重新刷新产品添加页面')
    }
};

// 点击不购买商品选择
var clickNoBugOption = function () {
    $('#advancedSettings .productID_select').on('click', function () {
        var div_ele = $(this).parent().parent();
        var select_sort = $(this).attr('name').split('_')[3];
        var option_value = $(this).find("option:selected").val();
        if (option_value == 'noBuy') {
            div_ele.html('');
            div_ele.append(`<label class="col-sm-1 control-label">不购买</label>
                            <div class="col-sm-4"><input type="text" name="pp2p_product_id_${select_sort}" 
                            class="form-control" value="" placeholder="这里输入不购买产品的描述">
                            </div><span class="glyphicon glyphicon-minus product-minus margin-top-8"></span>`);
            productMinus();
        }


    })
};

// 点击产品保存按钮
var clickProductBtn = function () {
    $('#product-btn').on('click', function () {
        $('#fm select[name="area"]').attr('name', "area_code");
        $('#fm select[name="city"]').attr('name', "city_code");
        var data = $('#fm').serialize();
        api.productAdd(data, productResponse)
    })
};

var productResponse = function (arg) {
    if (arg.status == 200) {
        layer.msg(arg.message);
        window.location.href = '/admin/product.html'
    } else {
        layer.msg(arg.error_message);
        $('#fm select[name="area_code"]').attr('name', "area");
        $('#fm select[name="city_code"]').attr('name', "city");
    }
};

// 上传图片
function UploadImage() {
    document.getElementById('iframe_image').onload = reloadIframe;
    document.getElementById('fm1').submit();
}

function reloadIframe() {
    var content = this.contentWindow.document.body.innerText;
    var obj = JSON.parse(content);
    var tag = document.createElement('img');
    // console.log(obj.data)
    tag.src = '/' + obj.data;
    tag.className = 'pro_image';
    document.getElementById('pro_image').innerHTML = '';
    document.getElementById('pro_image').appendChild(tag);
    $('#fm  input[name="p_t_imgae"]').val(obj.message);
    $('#pro_upload').css('display', 'none');
    $('#remove_image').css('display', 'block');
    $('#remove_image').removeClass('hide')
}
// 点击x 更换图片
function removeImg(ths) {
    layer.confirm('是否要更换封面？', {
            btn: ['是', '否'] //按钮
        },
        function (index) {
            $('#pro_image').text('');
            $('#remove_image').css('display', 'none');
            $('#pro_upload').css('display', 'block');
            layer.close(index);
        },
        function (index) {
            layer.close(index);
        });
};
// function clickBtn() {
//         $('#pg_content').on('click','btn-primary', function(){
//             var v1 = $('#pg_content .p_t_imgae').val();
//             if (v1){}
//             else {alert('请上传图片')}
//         })
//     }

