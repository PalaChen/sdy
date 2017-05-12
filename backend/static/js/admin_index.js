/**
 * Created by pala on 2017/3/29.
 */
$(function () {
    bindShowModalGenernal();
    bindUploadSave();
    bindOnlyClick();
    bindChangeInput();
    bindOnlyInputBtnClick();
    //bindGetMenu();
});

var clickState = 0;  //初始化点击状态

// 把label变成一个input框
function bindChangeInput() {
    $('#department_info .glyphicon-pencil').on('click', function () {
        var original_text = $(this).prev().text().trim();
        var nid = $(this).prev().attr('nid');
        var parent_div = $(this).parent().empty();
        var input_ele = document.createElement('input');
        input_ele.setAttribute('name', 'name');
        input_ele.setAttribute('class', 'input_info');
        input_ele.setAttribute('nid', nid);
        input_ele.setAttribute('for', 'department');
        input_ele.type = 'text';
        input_ele.value = original_text;
        parent_div.append(input_ele);
        parent_div.append("<a class='initialize btn glyphicon glyphicon-ok btn_send_add'>");
        parent_div.append("<a class='initialize btn glyphicon glyphicon-off'>");
        bindCloseChangeInput();
        bindOnlyInputBtnClick()
    })
}
// 取消修改，把输入框变成label标签
function bindCloseChangeInput() {
    $('#department_info .glyphicon-off').on('click', function () {
        var original_text = $(this).prevAll('input').val();
        var nid = $(this).prevAll('input').attr('nid');
        var parent_div = $(this).parent().empty();
        var label_ele = document.createElement('label');
        label_ele.setAttribute('class', 'label_for glyphicon glyphicon-menu-hamburger font_14');
        label_ele.setAttribute('nid', nid);
        label_ele.textContent = '   ' + original_text;
        parent_div.append(label_ele);
        parent_div.append('<a class="initialize btn glyphicon glyphicon-pencil">');
        parent_div.append('<a class="initialize btn glyphicon glyphicon-remove hide">');
        bindChangeInput();
    })
}


// 模态框
function bindShowModalGenernal() {
    // 上传轮播图
    $("#add_bxslider").click(function () {
        $("#Model_UploadInfo").modal('show');
        var type = $("#Model_UploadInfo").attr('for');
        var modal = "#Model_UploadInfo";
        bindUploadSave(modal, type)
    });
    // 文章分类模态框
    $('#add_category').click(function () {
        $('#Add_Ariticle_Info').modal('show');
    });
    // 通用模态框打开
    $('#add_Info').click(function () {
        $('#Model_AddInfo').modal('show');
    });
    // 通用模态框2打开
    $('#add_Info_1').click(function () {
        $('#Model_AddInfo_1').modal('show');
    });
    // 产品分类模态框
    $('#cat_add').click(function () {
        $('#Model_CategoryAddInfo').modal('show');
    });
    // 修改图片模态框
    $('#tb_content').on('click', '.glyphicon-pencil', function () {

        var type = $(this).parent().parent().attr('for');
        if (type == 'bxslider_edit') {
            $("#Model_UploadEditInfo").modal('show');
            get_Modal_Info($(this), type)
        }
        else if (type == 'p_category_edit') {
            var model = '#Model_EditInfo';
            $(model).modal('show');
        }
        else if (type == 'category') {
            var model = '#Model_EditInfo';
            $(model).modal('show');
        }
        else if (type == 'keyword') {
            var model = '#Model_EditInfo';
            $(model).modal('show');
        }
        get_Modal_Edit_Info($(this), model, type)
    });
    // 删除模态框
    $('#tb_content').on('click', '.glyphicon-remove', function () {
        $('#submit_del_con').modal('show');

        var type = $(this).parent().parent().attr('for');
        var nid = $(this).parent().parent().attr('nid');
        var modal = '#submit_del_con';

        Del_Confirm_Sub(modal, type, nid, $(this));

    });
    // 查看模态框
    $('#tb_content').on('click', '.glyphicon-search', function () {
        var model_type = $(this).parent().parent().attr('for');
        if (model_type == 'service_manage') {
            var nid = $(this).parent().parent().children().first().text();
            var order_id = $(this).parent().parent().children().eq(1).text();
            $('#Model_AddInfo input[name="order_serice"]').val(nid);
            $('#Model_AddInfo input[name="order"]').val(order_id);
            $('#Model_AddInfo').modal('show');
        }
    });
    // 订单分配查看订单业务进展
    $('#tb_content').on('click', '.btn-sm', function () {
        var model_type = $(this).parent().parent().attr('for');
        if (model_type == 'service_manage') {
            var nid = $(this).parent().parent().children().eq(1).text();
            var url = '/admin/service/order_business/' + nid + '.html';
            $.ajax({
                type: 'GET',
                url: url,
                dataType: 'json',
                success: function (arg) {
                    if (arg['status'] == 200) {
                        if (arg['tbbody']) {
                            for (var i = 0; i < arg['tbbody'].length; i++) {
                                var tr_ele = document.createElement('tr');
                                var td1 = document.createElement('td');
                                td1.innerHTML = arg['tbbody'][i]['process_name'];
                                var td2 = document.createElement('td');
                                td2.innerHTML = arg['tbbody'][i]['step_name'];
                                var td3 = document.createElement('td');
                                td3.innerHTML = arg['tbbody'][i]['employee_name'];
                                var td4 = document.createElement('td');
                                td4.innerHTML = arg['tbbody'][i]['date'];
                                tr_ele.append(td1);
                                tr_ele.append(td2);
                                tr_ele.append(td3);
                                tr_ele.append(td4);
                                $('#p_business_info').append(tr_ele)
                            }
                            $('#Model_ToView').modal('show');
                        }
                    }
                    else {
                        alert('非法操作')
                    }
                }
            })
        }

    })
}

// 发送一次请求
function bindOnlyClick() {
    // 添加文章栏目信息确认按钮
    $('#Add_Ariticle_Info .btn_save').click(function () {
        if (clickState == 1) {                //如果状态为1就什么都不做
        } else {
            clickState = 1;  //如果状态不是1  则添加状态 1
            type = $('#Add_Ariticle_Info').attr('for');
            modal = $('#Add_Ariticle_Info');
            if (type == 'keyword_add') {
                url = '/admin/keyword_add.html';
                data = $('#fm_keyword_add');
            }
            else if (type == 'category_add') {
                url = '/admin/category_add.html';
                data = $('#fm_category_add');
            }
            setTimeout(send_Ajax_AddInfo(url, data, modal), 3000);
        }
    });
    // 添加产品分类信息确认按钮
    $("#Model_CategoryAddInfo .btn_send_add").click(function () {
        if (clickState == 1) {                //如果状态为1就什么都不做
        } else {
            clickState = 1;  //如果状态不是1  则添加状态 1
            modal = $('#Model_CategoryAddInfo');
            type = modal.attr('for');

            if (type == 'category_add') {
                url = '/admin/product/category_add.html';
                data = $('#fm3_add');
            }
            setTimeout(send_Ajax_AddInfo(url, data, modal), 3000);
        }
    });
    // 通用添加信息
    $('#Model_AddInfo .btn_save').click(function () {
        if (clickState == 1) {                //如果状态为1就什么都不做
        } else {
            clickState = 1;
            modal = $('#Model_AddInfo');
            var model_type = modal.attr('for');
            data = $('#fm_body');
            if (model_type == 'nav_add') {
                url = '/admin/site/nav_add.html';
            }
            else if (model_type == 'org_add') {
                url = "/admin/org/deparment_add.html"
            }
            else if (model_type == 'service_manage') {
                url = '/admin/service/assign_employee.html'
            }
            else if (model_type == 'order_business') {
                url = '/admin/my_task/order_business_add.html'
            }
            else if (model_type == 'area_add') {
                url = '/admin/area_add.html'
            }
            setTimeout(send_Ajax_AddInfo(url, data, modal), 3000);
        }
    });
    // 通用添加信息1
    $('#Model_AddInfo_1 .btn_save').click(function () {
        if (clickState == 1) {                //如果状态为1就什么都不做
        } else {
            clickState = 1;
            modal = $('#Model_AddInfo_1');
            var model_type = modal.attr('for');
            var data = $('#fm_body_1');
            if (model_type == 'position') {
                var url = '/admin/org/position_add.html';
            }
            setTimeout(send_Ajax_AddInfo(url, data, modal), 3000);
        }
    });
    // 修改分类信息确认按钮
    $('#Model_EditInfo .btn_send_add').click(function () {
        if (clickState == 1) {                //如果状态为1就什么都不做
        } else {
            clickState = 1;  //如果状态不是1  则添加状态 1
            modal = $('#Model_EditInfo');
            type = modal.attr('for');

            if (type == 'p_category_edit') {
                url = '/admin/product/category_edit.html';
                data = $('#fm4_add');
            }
            else if (type == 'category_edit') {
                url = '/admin/category_edit.html';
                data = $('#fm_edit');
            }
            else if (type == 'keyword_edit') {
                url = '/admin/keyword_edit.html';
                data = $('#fm_edit');
            }
            setTimeout(send_Ajax_AddInfo(url, data, modal), 3000);
        }
    });
    // glyphicon-pencil my_task中修改具体业务步骤

};
// 输入框点击按钮发送请求信息
function bindOnlyInputBtnClick() {
    // 输入框点击按钮发送修改请求信息
    $('#department_info .btn_send_add').click(function () {
        if (clickState == 1) {                //如果状态为1就什么都不做
        } else {
            clickState = 1;
            var type = $(this).prev().attr('for');
            var name = $(this).prev().val();
            var nid = $(this).prev().attr('nid');
            var data = {'name': name, 'id': nid};
            if (type == 'department') {
                var url = '/admin/org/deparment_edit.html'
            }
            send_Input_Ajan_Info(url, data)
        }
    });
    $('#department_info .glyphicon-remove').on('click', function () {
        var nid = $(this).prevAll('label').attr('nid');
        var url = '/admin/org/deparment_del.html';
        var data = {'id': nid};
        send_Input_Ajan_Info(url, data)
    })
}
// 获取将要修改的信息到模态框
function get_Modal_Edit_Info(ths, modal, type) {
    //console.log(type);
    if (type == 'p_category_edit') {
        ths.prevAll().each(function () {
            if (ths.attr('for') != 'undefined') {
                var v = $(this).text().trim();
                var k = $(this).attr('for');
                console.log(k, v);
                $(modal + " input[name='" + k + "']").val(v);
            }
        });
        var v1 = ths.parent().parent().attr('prev_id');
        $(modal + " select[name='root_id']").val(v1);
        var v2 = ths.parent().parent().attr('nid');
        $(modal + " input[name='nid']").val(v2);
    }
    else {
        ths.parent().prevAll().each(function () {
            if (ths.attr('for') != 'undefined') {
                var v = $(this).text().trim();
                var k = $(this).attr('for');
                //console.log(k, v);
                $(modal + " input[name='" + k + "']").val(v);
            }
        })
    }
}

// 从表单获取信息填充到修改图片模态框中
function get_Modal_Info(ths, type) {
    var tds = ths.parent().siblings();
    var modal = "#Model_UploadEditInfo";
    for (var i = 0; i < tds.length - 1; i++) {
        k = tds.eq(i).attr('for');
        v = tds.eq(i).text().trim();
        if (k == 'status') {
            if (v == '上架') {
                v1 = 1;
            }
            else {
                v1 = 0;
            }
            $(modal + " input[name='" + k + "'][value='" + v1 + "']").prop('checked', 'checked');

        }
        else {
            $(modal + " input[name='" + k + "']").val(v);
        }

    }
    bindUploadSave(modal, type)
}

// 从表单中获取上传文件信息
function bindUploadSave(modal, type) {

    $(modal + ' .btn_Save').click(function () {
        if (clickState == 1) {
        }
        else {
            clickState = 1;
            //console.log(clickState);
            var file_obj = $(modal + ' .img_upload')[0].files[0];
            var data = new FormData();
            $(modal + ' .modal-body').find('input:text').each(function () {
                var k = $(this).attr('name');
                var v = $(this).val();
                data.append(k, v);
            });
            var v1 = $(modal + ' .modal-body').find("input[name='status']:checked").val();
            var csrf = $(modal + ' .modal-body').find("input[name='csrfmiddlewaretoken']").val();
            data.append('csrfmiddlewaretoken',csrf);
            data.append('status', v1);
            data.append('img', file_obj);

            if (type == 'bxslider_add') {
                var url = '/admin/site/bxslider_add';
            }
            else if (type == 'bxslider_edit') {
                var url = '/admin/site/bxslider_edit';

            }
            setTimeout(send_Add_Ajax_Info(url, data, modal), 5000);
        }
    })
}

// 上传文件ajax
function send_Add_Ajax_Info(url, data, modal) {
    $.ajax({
        url: url,
        type: "POST",
        data: data,
        processData: false,
        contentType: false,
        success: function (arg) {
            if (arg['status'] == true) {
                alert(arg['message']);
                $(modal).modal('hide');
                window.location.reload()
            }
            else {
                alert(arg['message'])
            }
            clickState = 0
        }
    });

}

// 删除确认
function Del_Confirm_Sub(modal, type, nid, ths) {
    if (type == 'bxslider_edit') {
        url = '/admin/site/bxslider_del/' + nid + '.html';
    }
    else if (type == 'category') {
        url = '/admin/category_del/' + nid + '.html';
    }
    else if (type == 'keyword') {
        url = '/admin/keyword_del/' + nid + '.html';
    }
    else if (type == 'p_category_edit') {
        url = '/admin/product/category_del/' + nid + '.html';
    }
    else if (type == 'product') {
        url = '/admin/product_del/' + nid + '.html';
    }
    $(modal + ' .btn-danger').click(function () {
        if (clickState == 1) {
        }
        else {
            clickState = 1;
            setTimeout(send_Del_Ajax_Info(modal, url, ths), 5000);
        }
    })
}

// 发送删除信息
function send_Del_Ajax_Info(modal, url, ths) {
    $.ajax({
        url: url,
        type: 'GET',
        success: function (arg) {
            if (arg == '成功') {
                $(modal).modal('hide');
                ths.parent().parent().addClass('hide');
                //alert('删除成功');
            }
            else {
                alert('非法操作')
            }
            clickState = 0
        }
    })

}

function send_Ajax_AddInfo(url, data, modal) {
    $.ajax({
        url: url,
        type: 'POST',
        data: $(data).serialize(),
        success: function (arg) {
            if (arg['status'] == 200) {
                modal.modal('hide');
                window.location.reload();
                //alert(arg['message']);
            } else {
                alert(arg['message'])
            }
            clickState = 0;
        }
    });
}

// 直接把输入框信息发送服务
function send_Input_Ajan_Info(url, data) {
    $.ajax({
        url: url,
        type: 'POST',
        data: data,
        dataType: 'json',
        success: function (arg) {
            console.log(arg);
            if (arg['status'] == 200) {
                window.location.reload();
                alert(arg['message']);
            } else {
                alert(arg['message'])
            }
            clickState = 0;
        }
    })
}


//function bindGetMenu() {
//    $.ajax({
//        url: '/admin/get_menu.html',
//        type: 'GET',
//        //dataType:'json',
//        success: function (arg) {
//            if (arg) {
//                $('#leftTop').parent().append(arg)
//            }
//        }
//    })
//}