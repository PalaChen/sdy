from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from app.forms.account import UserConsultationForm
from reposition import models, model_query, model_update, model_add
from utils.check_code import create_validate_code
from django.db.models import Q
from utils.menu import get_cate_list, user_info


# city_obj = models.RegionalManagement.objects.filter(Q(r_code__isnull=False)).all()
# current_city = '佛山市'
# request.session['global_variale'] = {'city_obj': city_obj, 'current_city': current_city}


def index(request):
    user_dict = user_info(request)
    default_city = request.session.get('default_city')
    title = '盛德业,注册公司,代理记账,佛山商标注册,佛山公司注册,顺德注册公司,佛山创业法律服务，佛山记账报税，广东佛山肇庆江门中山韶关公司注册'
    description = '盛德业公司是一家以广东公司注册,佛山注册公司,佛山工商注册,佛山代理记账,佛山财税咨询,佛山商标注册专项审批为核心业务,为企事业单位提供相关咨询服务的一站式专业服务机构，我公司服务周到，收费合理，热忱欢迎新老客户，来人来电，咨询合作，盛德业统一客服热线4008813338！'
    keywords = '公司注册，佛山注册公司，佛山记账报税，佛山代理记账，佛山工商注册，佛山商标注册，顺德公司注册，顺德注册公司，南海公司注册，南海注册公司，禅城公司注册，佛山代办执照，顺德代办营业执照，佛山注册公司流程，佛山进出口退税，佛山食品经营许可证'
    is_login = None
    if request.method == 'GET':
        bxSlider = models.Bxslider.objects.filter(status=1).order_by('weight').all()
        articles_list = models.Articles.objects.order_by('-ctime').values('id', 'category_id', 'title')[4:10]
        articles_images_obj = models.Articles.objects.filter(is_top=0).order_by('-ctime')[0:4]
        nav_list = models.IndexNav.objects.order_by('-weight').values('name', 'url', 'ishot')[0:7]
        city_obj = models.RegionalManagement.objects.filter(Q(r_code__isnull=False)).all()
        if default_city['area_id']:
            packages_obj = models.Package.objects.filter(status=1, area_id=default_city['area_id']).order_by('weight')[
                           0:3]
        else:
            packages_obj = None
        # 推荐产品列表
        recommend_obj = models.Products.objects.filter(p_top=1).order_by('-p_ctime')[0:9]
        ad_obj = models.Banner.objects.filter(status=1).order_by('position')
        cate_list = get_cate_list()
        cookie = request.COOKIES
        is_login = request.session.get('is_login')
        from django.template import loader
        # content = loader.render_to_string('user/user_index.html')
        # print(content)
        d = {'bxSlider': bxSlider, 'cate_list': cate_list,
             'cookie': cookie, 'is_login': is_login,
             'nav_list': nav_list, 'articles_list': articles_list,
             'user_info': user_dict, 'city_obj': city_obj,
             'articles_images_obj': articles_images_obj,
             'default_city': default_city, 'title': title,
             'description': description, 'keywords': keywords,
             'recommend_obj': recommend_obj, 'packages_obj': packages_obj,
             'ad_obj': ad_obj}
        return render(request, 'index.html', d)


def get_userInfo(request):
    result_dict = {'status': 200, 'message': None, 'data': None}
    if request.method == 'POST':
        form_obj = UserConsultationForm(request.POST)
        if form_obj.is_valid():
            data = form_obj.cleaned_data
            # try:

            Consulation_obj = models.UserConsultation.objects.filter(phone=request.POST.get('phone')).first()
            if not Consulation_obj:
                data['type'] = 0
                data['isknow'] = 2
                models.UserRecommend.objects.get_or_create(**data)
                # except Exception as e:
                #     result_dict['status'] = 401
                #     result_dict['message'] = '非法数据，输入无效。'
        else:
            result_dict['status'] = 401
            result_dict['message'] = list(form_obj.errors.values())[0][0]
        return JsonResponse(result_dict)


# 切换城市
def switch_city(request, city_id):
    city_obj = models.RegionalManagement.objects.filter(id=city_id).first()
    if city_obj:
        area_obj = models.RegionalManagement.objects.filter(p_code=city_obj.code).first()
        if area_obj:
            area_id = area_obj.id
        else:
            area_id = ''
        request.session['default_city'] = {'city_id': city_obj.id, 'city': city_obj.name,
                                           'area_id': area_id}

    return redirect('web_index')
