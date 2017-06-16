from django.shortcuts import render, redirect, reverse, HttpResponse
from django.http import JsonResponse
from backend.forms.forms_site import BxsilderForm
from backend.forms.forms_article import ArticleForm, CategoryForm, KeywordForm, ArticleSearchForm
from reposition import models
from reposition import model_query, model_add, modal_del
from utils.pager import paginator
from backend.forms.product import ImageForm
from utils.upload_image import save_image
from utils.upload_image import ckedit_upload_image
from utils.login_admin import login_required, permission
from cxmadmin import base

web_title = {'articles': '文章管理',
             'article_add': '添加文章',
             'article_edit': '修改文章',
             'category': '栏目管理',
             'category_add': '栏目添加',
             'keywords': '标签管理',
             'keyword_add': '标签添加'}

result_dict = {'status': 200, 'message': None, 'data': 'None'}


def is_author(func):
    def inner(request, *args, **kwargs):
        employee_id = request.session.get('user_info')['employee_id']
        author_obj = models.Author.objects.filter(employee_id=employee_id).first()
        if not author_obj:
            return redirect(reverse('author_add'))
        else:
            return func(request, *args, **kwargs)

    return inner


@login_required
# @permission
@is_author
def articles(request, *args, **kwargs):
    action_list = kwargs.get('action_list')
    menu_string = kwargs.get('menu_string')
    form = ArticleSearchForm()
    articles_obj = models.Articles.objects.all().order_by('-ctime')
    posts = paginator(request, articles_obj)
    return render(request, 'articles/articles.html', {'posts': posts,
                                                      'menu_string': menu_string,
                                                      'title': web_title['articles'],
                                                      'form': form,
                                                      })


@login_required
def author_add(request):
    title = '绑定作者'
    error = ''
    if request.method == 'POST':
        name = request.POST.get('name')
        employee_id = request.session.get('user_info')['employee_id']
        author_obj = models.Author.objects.filter(name=name).first()
        if not author_obj:
            models.Author.objects.create(name=name, employee_id=employee_id)
            return redirect('articles_all')
        else:
            error = '改名字已被使用'
    info_dict = {'title': title,
                 'error': error,}
    return render(request, 'articles/author_add.html', info_dict)


@login_required
def articles_search(req):
    form = ArticleSearchForm(req.POST or None)
    if req.method == 'POST':
        if form.is_valid():
            category_id = form.cleaned_data.get('category_id')
            status = form.cleaned_data.get('status')
            is_top = form.cleaned_data.get('is_top')
            text = form.cleaned_data.get('text')
            articles_obj = models.Articles.objects.filter(category_id=category_id, status=status).all()
            posts = paginator(req, articles_obj)
            return render(req, 'articles/articles.html', {'posts': posts,
                                                          'form': form,
                                                          'title': web_title['articles'],
                                                          })
    return redirect('articles_all')


def article_model(req, form, author_obj):
    content = form.cleaned_data.get('content')
    article_info = form.cleaned_data
    article_info['author_id'] = author_obj.id
    del article_info['content']
    del article_info['keyword']
    return content, article_info


@login_required
@permission
def article_add(req, *args, **kwargs):
    menu_string = kwargs.get('menu_string')
    form = ArticleForm(req.POST or None)
    error = None
    if req.method == 'POST':
        if form.is_valid():
            employee_id = req.session.get('user_info')['employee_id']
            author_obj = models.Author.objects.filter(employee_id=employee_id).first()
            content, article_info = article_model(req, form, author_obj)
            # print(article_info)
            article_obj = models.Articles.objects.create(**article_info)
            models.ArticlesDetails.objects.create(article=article_obj, content=content)
            author_obj.counts += 1
            author_obj.save()
            return redirect('articles_all')
        else:
            error = list(form.errors.values())[0][0]
    return render(req, 'articles/article_add.html', {'form': form,
                                                     'error': error,
                                                     'menu_string': menu_string,
                                                     'title': web_title['article_add'],
                                                     })


@login_required
@permission
def article_edit(req, article_id, *args, **kwargs):
    menu_string = kwargs.get('menu_string')
    article_info = models.Articles.objects.filter(id=article_id).select_related('articlesdetails').first()
    form = ArticleForm(req.POST or None)
    error = None
    if req.method == 'POST':
        if form.is_valid():
            content, article_info = article_model(req, form)
            models.Articles.objects.filter(id=article_id).update(**article_info)
            models.ArticlesDetails.objects.filter(article_id=article_id).update(content=content)
            return redirect('articles_all')
        else:
            error = list(form.errors.values())[0][0]
    return render(req, 'articles/article_edit.html', {'form': form,
                                                      'error': error,
                                                      'menu_string': menu_string,
                                                      'article_info': article_info,
                                                      'title': web_title['article_edit'],})


@login_required
@permission
def article_del(req, articled_id, *args, **kwargs):
    res = modal_del.query_del(req, models.Articles, articled_id)
    return HttpResponse(res)


@login_required
def article_image(request):
    res_dict = {'status': True, 'data': None, 'message': None}
    if request.method == 'POST':
        files = ImageForm(request.POST, request.FILES)
        if files.is_valid():
            img = request.FILES.get('img')
            data = save_image(img)
            if data:
                data['ul_employee_id'] = request.session.get('user_info')['employee_id']
                image_obj = models.ArticlesCoverImage.objects.create(**data)
                res_dict['data'] = data['ul_url']
                res_dict['message'] = image_obj.id
                return JsonResponse(res_dict)
    res_dict['status'] = False
    return JsonResponse(res_dict)


@login_required
@permission
@is_author
def category(request, *args, **kwargs):
    action_list = kwargs.get('action_list')
    menu_string = kwargs.get('menu_string')
    form = CategoryForm()
    category_obj = model_query.query_all(models.ArticlesCategory)
    posts = paginator(request, category_obj)
    return render(request, 'articles/article_category.html', {'title': web_title['category'],
                                                              'menu_string': menu_string,
                                                              'form': form,
                                                              'posts': posts,
                                                              })


@login_required
@permission
def category_add(request, *args, **kwargs):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            author_obj = models.Author.objects.filter(
                employee_id=request.session.get('user_info')['employee_id']).first()
            data['author_id'] = author_obj.id
            models.ArticlesCategory.objects.create(**data)
            result_dict['message'] = '文章分类添加成功'
            return JsonResponse(result_dict)
        else:
            result_dict['message'] = list(form.errors.values())[0][0]
    result_dict['status'] = 201
    return JsonResponse(result_dict)


@login_required
@permission
def category_edit(request, *args, **kwargs):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            id = request.POST.get('id')
            data = form.cleaned_data
            author_obj = models.Author.objects.filter(
                employee_id=request.session.get('user_info')['employee_id']).first()
            data['author_id'] = author_obj.id
            category_obj = models.ArticlesCategory.objects.filter(id=id).first()
            if category_obj:
                models.ArticlesCategory.objects.filter(id=id).update(**data)
                result_dict['status'] = 200
                result_dict['message'] = '文章分类修改成功'
                return JsonResponse(result_dict)
            else:
                result_dict['message'] = '非法输入数据'
        else:
            result_dict['message'] = list(form.errors.values())[0][0]
    result_dict['status'] = 800
    return JsonResponse(result_dict)


@login_required
@permission
def category_del(req, id, *args, **kwargs):
    res = modal_del.query_del(req, models.ArticlesCategory, id)
    return HttpResponse(res)


@login_required
@permission
@is_author
def keywords(request, *args, **kwargs):
    action_list = kwargs.get('action_list')
    menu_string = kwargs.get('menu_string')
    form = KeywordForm()
    keyword_obj = model_query.query_all(models.ArticlesTag)
    posts = paginator(request, keyword_obj)
    return render(request, 'articles/article_keyword.html', {'title': web_title['keywords'],
                                                             'menu_string': menu_string,
                                                             'form': form,
                                                             'posts': posts,
                                                             })


@login_required
@permission
def keyword_add(request, *args, **kwargs):
    if request.method == 'POST':
        form = KeywordForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            author_obj = models.Author.objects.filter(
                employee_id=request.session.get('user_info')['employee_id']).first()
            data['author_id'] = author_obj.id
            models.ArticlesTag.objects.create(**data)
            result_dict['status'] = 200
            result_dict['message'] = '文章标签添加成功'
            return JsonResponse(result_dict)
        else:
            result_dict['message'] = list(form.errors.values())[0][0]
    result_dict['status'] = 201
    return JsonResponse(result_dict)


@login_required
@permission
def keyword_edit(request, *args, **kwargs):
    if request.method == 'POST':
        form = KeywordForm(request.POST)
        if form.is_valid():
            id = request.POST.get('id')
            data = form.cleaned_data
            author_obj = models.Author.objects.filter(
                employee_id=request.session.get('user_info')['employee_id']).first()
            data['author_id'] = author_obj.id
            tag_obj = models.ArticlesTag.objects.filter(id=id).first()
            if tag_obj:
                models.ArticlesTag.objects.filter(id=id).update(**data)
                result_dict['message'] = '文章标签修改成功'
            else:
                result_dict['status'] = 800
                result_dict['message'] = '非法数据'

        else:
            result_dict['status'] = 800
            result_dict['message'] = list(form.errors.values())[0][0]

    return JsonResponse(result_dict)


@login_required
@permission
def keyword_del(req, id, *args, **kwargs):
    res = modal_del.query_del(req, models.ArticlesTag, id)
    return HttpResponse(res)
