from django.template import Library
from django.utils.safestring import mark_safe

register = Library()


@register.simple_tag
def wap_package_price(pp2p_dict, pp, num):
    """
    <div id="tab1" class="weui-tab__bd-item other_priceweui-tab__bd-item--active"></div>
    """
    html_ele = ''
    n = 1
    num = num * 8
    for pp2p in pp2p_dict[pp.id]:
        html_ele += '<div id="tab{}" class="weui-tab__bd-item other_price'.format(num)
        if n == 1:
            html_ele += ' weui-tab__bd-item--active">'
        else:
            html_ele += '">'

        if pp2p.pp2p_product:
            html_ele += '￥{}</div>'.format(pp2p.pp2p_product.p_price)

        else:
            html_ele += '</div>'
        n += 1
        num += 1
    return mark_safe(html_ele)


@register.simple_tag
def wap_package_info(pp2p_dict, pp, num):
    html_ele = ''
    n = 1
    num = num * 8
    for pp2p in pp2p_dict[pp.id]:
        html_ele += '<a class="weui-navbar__item'
        if n == 1:
            html_ele += ' weui-bar__item--on"'
        else:
            html_ele += '"'

        if pp2p.pp2p_product:
            html_ele += 'href="#tab{}" nid="{}" price="{}">{}</a>'.format(num, pp2p.id, pp2p.pp2p_product.p_price,
                                                                          pp2p.pp2p_product)
        else:
            html_ele += 'href="#tab{}">{}</a>'.format(num,
                                                      pp2p.pp2p_notbuy)
        n += 1
        num += 1
    return mark_safe(html_ele)
