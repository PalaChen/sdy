/**
 * Created by pala on 2017/3/29.
 */
$(function () {
    bindShowModal();
    bindUploadSave();
    bindOnlyClick()
});

var clickState = 0;//初始化点击状态

function bindOnlyClick() {
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
    })
}

// 模态框
function bindShowModal() {
    // 上传轮播图
    $("#add_bxslider").click(function () {
        $("#Model_AddInfo").modal('show');
        var type = $("#Model_AddInfo").attr('for');
        var modal = "#Model_AddInfo";
        bindUploadSave(modal, type)
    });
    $('#add_category').click(function () {
        $('#Add_Ariticle_Info').modal('show');
    });
    $('#tb_content').on('click', '.glyphicon-pencil', function () {

        var type = $(this).parent().parent().attr('for');
        $("#Model_EditInfo").modal('show');
        var modal = "#Model_EditInfo";
        get_Modal_Info($(this), modal, type)
    });
    $('#tb_content').on('click', '.glyphicon-remove', function () {
        $('#submit_del_con').modal('show');

        var type = $(this).parent().parent().attr('for');
        var nid = $(this).parent().parent().attr('nid');
        var modal = '#submit_del_con';
        Del_Confirm_Sub(modal, type, nid)
    })

}
// 从表单获取信息填充到修改模态框中
function get_Modal_Info(ths, modal, type) {
    var tds = ths.parent().siblings();
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
        } else {
            console.log($(modal + ' .img_upload'));
            file_obj = $(modal + ' .img_upload')[0].files[0];
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
                url = '/admin/site/bxslider_add';
                modal = $('#Model_AddInfo');
            }
            else {
                url = '/admin/site/bxslider_edit';
                modal = $('#Model_EditInfo');
            }
            setTimeout(send_Add_Ajax_Info(url, data, modal), 5000);
        }
    })
}

// 上传文件ajax
function send_Add_Ajax_Info(url, data, modal) {
    clickState = 0;
    $.ajax({
        url: url,
        type: "POST",
        data: data,
        processData: false,
        contentType: false,
        success: function (arg) {
            if (arg['status'] == true) {
                alert('上传图片成功');
                console.log(modal);
                modal.modal('hide');
                window.location.reload()
            }
            else {
                alert(arg['message'])
            }
        }

    })
}

// 删除确认
function Del_Confirm_Sub(modal, type, nid) {
    if (type == 'bxslider_upload') {
        url = '/admin/site/bxslider_del/' + nid;
    }
    $(modal + ' .btn-danger').click(function () {
        bindOnlyClick(send_Del_Ajax_Info(modal));
    })
}

// 发送删除信息
function send_Del_Ajax_Info(modal) {
    $.ajax({
        url: url,
        type: 'GET',
        success: function (arg) {
            if (arg == '成功') {
                alert('删除成功');
                $(modal).modal('hide')
            }
            else {
                alert('非法操作')
            }
        }
    })

}

function send_Ajax_AddInfo(url, data, modal) {
    $.ajax({
        url: url,
        type: 'POST',
        data: data.serialize(),
        success: function (arg) {
            if (arg['status'] == 200) {
                modal.modal('hide');
                alert('添加成功');
                window.location.reload();
            } else {
                alert(arg['message'])
            }
        }
    });
    clickState = 0

}
