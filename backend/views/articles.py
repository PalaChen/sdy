from django.shortcuts import render, redirect, reverse, HttpResponse
from django.http import JsonResponse
from backend.forms.forms_site import BxsilderForm
from backend.forms.forms_article import ArticleForm, CategoryForm, KeywordForm, ArticleSearchForm
from reposition import models
from reposition import model_query, model_add, modal_del
from utils.pager import paginator
from utils.upload_image import ckedit_upload_image
from utils.login_admin import login_required,permission


web_title = {'articles': '文章管理',
             'article_add': '添加文章',
             'article_edit': '修改文章',
             'category': '栏目管理',
             'category_add': '栏目添加',
             'keywords': '标签管理',
             'keyword_add': '标签添加'}

result_dict = {'status': 200, 'message': None, 'data': 'None'}

@login_required
@permission
def articles(req,*args, **kwargs):
    action_list = kwargs.get('action_list')
    menu_string = kwargs.get('menu_string')
    form = ArticleSearchForm()
    articles_obj = models.Articles.objects.all().order_by('-ctime')
    posts = paginator(req, articles_obj)
    return render(req, 'articles/articles.html', {'posts': posts,
                                                  'menu_string': menu_string,
                                                  'title': web_title['articles'],
                                                  'form': form,
                                                  })

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


def article_model(req, form):
    employee_id = req.session.get('employee_id')
    content = form.cleaned_data.get('content')
    article_info = form.cleaned_data
    article_info['author_id'] = employee_id
    del article_info['content']
    del article_info['keyword']

    return content, article_info

@login_required
def article_add(req):
    form = ArticleForm(req.POST or None)
    error = None
    if req.method == 'POST':
        if form.is_valid():
            content, article_info = article_model(req, form)
            article = models.Articles.objects.create(**article_info)
            models.ArticlesDetails.objects.create(article=article, content=content)
            return redirect('articles_all')
        else:
            error = list(form.errors.values())[0][0]
    return render(req, 'articles/article_add.html', {'form': form,
                                                     'error': error,
                                                     'title': web_title['article_add'],
                                                     })

@login_required
def article_edit(req, article_id):
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
                                                      'article_info': article_info,
                                                      'title': web_title['article_edit'],})

@login_required
def article_image(req):
    res_dict = ckedit_upload_image(req, 'article')
    return JsonResponse(res_dict)

@login_required
@permission
def category(req, *args, **kwargs):
    action_list = kwargs.get('action_list')
    menu_string = kwargs.get('menu_string')
    form = CategoryForm()
    category_obj = model_query.query_all(models.ArticlesCategory)
    posts = paginator(req, category_obj)
    return render(req, 'articles/article_category.html', {'title': web_title['category'],
                                                          'menu_string': menu_string,
                                                          'form': form,
                                                          'posts': posts,
                                                          })

@login_required
def category_add(req):
    if req.method == 'POST':
        form = CategoryForm(req.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['author_id'] = req.session.get('employee_id')
            models.ArticlesCategory.objects.create(**data)
            result_dict['message'] = '文章分类添加成功'
            return JsonResponse(result_dict)
        else:
            result_dict['message'] = list(form.errors.values())[0][0]
    result_dict['status'] = 201
    return JsonResponse(result_dict)

@login_required
def category_del(req, id):
    res = modal_del.query_del(req, models.ArticlesCategory, id)
    return HttpResponse(res)

@login_required
@permission
def keywords(req, *args, **kwargs):
    action_list = kwargs.get('action_list')
    menu_string = kwargs.get('menu_string')
    form = KeywordForm()
    keyword_obj = model_query.query_all(models.ArticlesTag)
    posts = paginator(req, keyword_obj)
    return render(req, 'articles/article_keyword.html', {'title': web_title['keywords'],
                                                         'menu_string': menu_string,
                                                         'form': form,
                                                         'posts': posts,
                                                         })

@login_required
def keyword_add(req):
    if req.method == 'POST':
        form = KeywordForm(req.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['author_id'] = req.session.get('employee_id')
            models.ArticlesTag.objects.create(**data)
            result_dict['message'] = '文章标签添加成功'
            return JsonResponse(result_dict)
        else:
            result_dict['message'] = list(form.errors.values())[0][0]
    result_dict['status'] = 201
    return JsonResponse(result_dict)

@login_required
def keyword_del(req, id):
    res = modal_del.query_del(req, models.ArticlesTag, id)
    return HttpResponse(res)
