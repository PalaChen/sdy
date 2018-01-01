from django.template import Library
from django.utils.safestring import mark_safe

register = Library()


@register.simple_tag
def package_info(n, pp2p_dict, pp):
    html_ele = ''
    for pp2p in pp2p_dict[pp.id]:
        if pp2p.pp2p_product:

            html_ele += '<li id="t-buyProduct_{}_{}" class="t-buyProduct_{}">' \
                        '   <a href="javascript:;" onclick="addProduct({},{},1,{})">{}</a>' \
                        '   <span>{}</span><i></i>' \
                        '</li>' \
                        '<li id="buyP_{}_{}" style="display:none;">' \
                        '   <div class="floatLeft cartName" style="padding-top:0">' \
                        '       <p>{}</p>' \
                        '   </div>' \
                        '   <div class="floatLeft cartDel">' \
                        '       <a href="javascript:void(0);" onclick="deleteProduct({}, {}, 1);"></a>' \
                        '   <div>' \
                        '</li>'.format(n, pp2p.pp2p_product.id, n,
                                       n, pp2p.pp2p_product.id, pp2p.pp2p_product.p_price, pp2p.pp2p_product,
                                       pp2p.pp2p_description, n, pp2p.pp2p_product.id, pp2p.pp2p_product,
                                       n, pp2p.pp2p_product.id,
                                       )
        else:
            html_ele += '<li  id="t-buyProduct_{}_0" class="t-buyProduct_{}">' \
                        '   <a href="javascript:;" onclick="addProduct({},0,1,0)">{}</a>' \
                        '   <span>{}</span><i></i>' \
                        '</li>'.format(
                n, n, n,
                pp2p.pp2p_notbuy,
                pp2p.pp2p_description)
    return mark_safe(html_ele)

