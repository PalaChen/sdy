from django.template import Library
from django.utils.safestring import mark_safe
import datetime, time

register = Library()


@register.simple_tag
# 筛选信息
def build_filter_ele(filter_column, admin_class):
    column_obj = admin_class.model._meta.get_field(filter_column)
    # print("column obj:", column_obj)
    filter_verboseName = get_column_verboseName(filter_column, admin_class)
    # print('filter_verboseName', filter_verboseName)
    filter_ele = "<div class='form-group marR20'><label class='marR10'>{}</label>".format(filter_verboseName)
    filter_ele += "<select class='form-control' name='{}'>".format(filter_column)
    try:
        # filter_ele = "<div class='form-group marR20'><lable>{}</label><select class='form-control' name='{}'>".format(
        #     filter_verboseName, filter_column)
        for choice in column_obj.get_choices():
            selected = ''
            if filter_column in admin_class.filter_condtions:  # 当前字段被过滤了
                if str(choice[0]) == admin_class.filter_condtions.get(filter_column):  # 当前值被选中了
                    selected = 'selected'
                    # print('selected......')

            option = "<option value='%s' %s>%s</option>" % (choice[0], selected, choice[1])
            filter_ele += option
    except AttributeError as e:
        print("err", e)
        # filter_ele = "<div class='form-group marR20'><label>{}</label><select class='form-control' name='{}__gte'>".format(
        #     filter_verboseName, filter_column)
        if column_obj.get_internal_type() in ('DateField', 'DateTimeField'):
            time_obj = datetime.datetime.now()
            time_list = [
                ['', '------'],
                [time_obj, 'Today'],
                [time_obj - datetime.timedelta(7), '七天内'],
                [time_obj.replace(day=1), '本月'],
                [time_obj - datetime.timedelta(90), '三个月内'],
                [time_obj.replace(month=1, day=1), 'YearToDay(YTD)'],
                ['', 'ALL'],
            ]

            for i in time_list:
                selected = ''
                time_to_str = '' if not i[0] else  "%s-%s-%s" % (i[0].year, i[0].month, i[0].day)
                if "%s__gte" % filter_column in admin_class.filter_condtions:  # 当前字段被过滤了
                    print('-------------gte')
                    if time_to_str == admin_class.filter_condtions.get("%s__gte" % filter_column):  # 当前值被选中了
                        selected = 'selected'
                option = "<option value='%s' %s>%s</option>" % \
                         (time_to_str, selected, i[1])
                filter_ele += option

    filter_ele += "</select></div>"
    return mark_safe(filter_ele)


@register.simple_tag
def get_column_verboseName(field_name, admin_class):
    field = admin_class.model._meta.get_field(field_name).verbose_name
    if field:
        return field
    else:
        return field_name


@register.simple_tag
# 主体内容信息
def build_table_row(obj, admin_class):
    """生成一条记录的html element"""

    ele = ""
    if admin_class.list_display:
        for index, column_name in enumerate(admin_class.list_display):

            column_obj = admin_class.model._meta.get_field(column_name)

            if column_obj.choices:  # get_xxx_display
                column_data = getattr(obj, 'get_%s_display' % column_name)()
            else:
                column_data = getattr(obj, column_name)

            td_ele = "<td>{}</td>".format(column_data)
            if index == 0:
                td_ele = "<td>{}</td>".format(column_data)
            ele += td_ele
    else:
        td_ele = "<td>{}</td>".format(obj)
        ele += td_ele
    return mark_safe(ele)


@register.simple_tag
# 显示类名
def get_model_name(admin_class):
    return admin_class.model._meta.model_name.upper()


@register.simple_tag
# 表头中每个字段点击排序后样式
def get_sorted_column(column, sorted_column, forloop):
    # sorted_column={'name':'-0'}
    # 如果column在sorted_column中，说明这一列被排序
    # 判断上一次的排序是什么，本次取反，如上次是正序，本次是反序
    if column in sorted_column:
        last_sort_index = sorted_column[column]
        if last_sort_index.startswith('-'):
            this_time_sort_index = last_sort_index.strip('-')
        else:
            this_time_sort_index = '-{}'.format(last_sort_index)
        return this_time_sort_index
    return forloop


@register.simple_tag
# 凭借筛选的字段,赋值给换页码的链接上
def render_filtered_args(admin_class, render_html=True):
    if admin_class.filter_condtions:
        ele = ''
        for k, v in admin_class.filter_condtions.items():
            ele += '&{}={}'.format(k, v)
            if render_html:
                return mark_safe(ele)
            else:
                return ele
    else:
        return ''


@register.simple_tag
def render_sorted_arrow(column, sorted_column):
    # 这一列被排序
    if column in sorted_column:
        last_sort_index = sorted_column[column]
        if last_sort_index.startswith('-'):
            arrow_direction = 'bottom'
        else:
            arrow_direction = 'top'
        ele = '''<span class="glyphicon glyphicon-triangle-%s" aria-hidden="true"></span>''' % arrow_direction
        return mark_safe(ele)
    return ''


# 分页
@register.simple_tag
def render_paginator(querysets, admin_class, sorted_column):
    ele = '''
      <ul class="pagination">
    '''
    if querysets.has_previous():
        has_p_ele = """<li><a href="?_page={}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>""".format(
            querysets.previous_page_number())
        ele += has_p_ele

    for i in querysets.paginator.page_range:

        if abs(querysets.number - i) < 2:  #
            active = ''
            # 当前页
            if querysets.number == i:
                active = 'active'
            filter_ele = render_filtered_args(admin_class)

            # 参数
            sorted_ele = ''
            if sorted_column:
                sorted_ele = '&_o=%s' % list(sorted_column.values())[0]

            p_ele = '''<li class="%s"><a href="?_page=%s%s%s">%s</a></li>''' % (active, i, filter_ele, sorted_ele, i)

            ele += p_ele

    if querysets.has_next():
        has_n_ele = """<li><a href="?_page={}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>""".format(
            querysets.next_page_number())
        ele += has_n_ele
    ele += "</ul>"

    return mark_safe(ele)


@register.simple_tag
def get_current_sorted_column_index(sorted_column):
    if sorted_column:
        current_sorted_column = list(sorted_column.values())[0]
        return current_sorted_column
    else:
        return ''


@register.simple_tag
def get_obj_field_val(form_obj, field):
    '''返回model obj具体字段的值'''
    print('field-->',field)
    return getattr(form_obj.instance, field)


@register.simple_tag
def get_available_m2m_data(field_name, form_obj, admin_class):
    """返回的是m2m字段关联表的所有数据"""

    field_obj = admin_class.model._meta.get_field(field_name)
    obj_list = set(field_obj.related_model.objects.all())

    selected_data = set(getattr(form_obj.instance, field_name).all())

    return obj_list - selected_data


@register.simple_tag
def get_selected_m2m_data(field_name, form_obj, admin_class):
    """返回已选的m2m数据"""

    selected_data = getattr(form_obj.instance, field_name).all()

    return selected_data


@register.simple_tag
def display_all_related_objs(obj):
    """
    显示要被删除对象的所有关联对象
    :param obj:
    :return:
    """
    # 生成的代码是ul套ul
    ele = "<ul>"

    for reversed_fk_obj in obj._meta.related_objects:

        # 获取反向关联的表名
        related_table_name = reversed_fk_obj.name
        # 字符串组合
        related_lookup_key = "%s_set" % related_table_name
        # 反向查询所有关联的数据
        if hasattr(obj, related_lookup_key):
            related_objs = getattr(obj, related_lookup_key).all()
            show_table_name = related_table_name
            for line in related_objs:
                if not line:
                    show_table_name = related_table_name
                else:
                    show_table_name = line._meta.verbose_name

            ele += "<li>{}<ul> ".format(show_table_name)
            # 判断类型是否等于多对多
            # ManyToMany不需要深入查找
            if reversed_fk_obj.get_internal_type() == "ManyToManyField":
                for i in related_objs:
                    ele += "<li><a href='/cxmadmin/{}/{}/{}/change/'>{}</a>   记录里与[{}]的相关数据将被删除</li>".format(
                        i._meta.app_label, i._meta.model_name, i.id, i, obj)
            else:
                for i in related_objs:
                    ele += "<li><a href='/cxmadmin/{}/{}/{}/change/'>{}</a></li>".format(i._meta.app_label,
                                                                                         i._meta.model_name,
                                                                                         i.id, i)
                    ele += display_all_related_objs(i)
            ele += "</ul></li>"
    ele += "</ul>"
    return ele
