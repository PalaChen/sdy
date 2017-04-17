/**
 * Created by pala on 2017/3/29.
 */
$(function () {
    bindShowModal();
    bindUploadSave();
    bindOnlyClick()
});

clickState = 0;//初始化点击状态
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
    // 添加分类信息确认按钮
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
            type = modal.attr('for');
            data = $('#fm_body');
            if (type == 'nav_add') {
                url = '/admin/site/nav_add.html';
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
            setTimeout(send_Ajax_AddInfo(url, data, modal), 3000);
        }
    })
}

// 模态框
function bindShowModal() {
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
        get_Modal_Edit_Info($(this), model, type)
    });
    // 删除模态框
    $('#tb_content').on('click', '.glyphicon-remove', function () {
        $('#submit_del_con').modal('show');

        var type = $(this).parent().parent().attr('for');
        var nid = $(this).parent().parent().attr('nid');
        var modal = '#submit_del_con';

        Del_Confirm_Sub(modal, type, nid, $(this));

    })

}

// 获取将要修改的信息到模态框
function get_Modal_Edit_Info(ths, modal, type) {
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
        $(modal + " select[name='cate_rootid']").val(v1);
        var v2 = ths.parent().parent().attr('nid');
        $(modal + " input[name='nid']").val(v2);
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
            console.log(clickState);
            var file_obj = $(modal + ' .img_upload')[0].files[0];
            var data = new FormData();
            $(modal + ' .modal-body').find('input:text').each(function () {
                var k = $(this).attr('name');
                var v = $(this).val();
                data.append(k, v);
            });
            var v1 = $(modal + ' .modal-body').find("input[name='status']:checked").val();
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
                alert('删除成功');
                $(modal).modal('hide');
                ths.parent().parent().addClass('hide');

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
                alert(arg['message']);
                window.location.reload();
            } else {
                alert(arg['message'])
            }
            clickState = 0;
        }
    });


}
