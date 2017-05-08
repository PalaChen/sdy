from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from reposition import models
from utils.pager import CustonPaginator

title_dict = {'index': '新闻资讯'}
hot_articles_obj = models.Articles.objects.order_by('-views')[0:5]


def paginator(req, obj):
    current_page = req.GET.get('p')
    paginator = CustonPaginator(current_page, 9, obj, 3)
    try:
        posts = paginator.page(current_page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return posts


def index(req):
    user_info = req.session.get('user_info')
    category_id = 1
    is_login = req.session.get('is_login')
    articles_obj = models.Articles.objects.all().order_by('-ctime')
    posts = paginator(req, articles_obj)
    category_boj = models.ArticlesCategory.objects.all()
    return render(req, 'news/news_index.html', {'posts': posts,
                                                'title': title_dict['index'],
                                                'hot_articles_obj': hot_articles_obj,
                                                'category_boj': category_boj,
                                                'category_id': category_id,
                                                'is_login': is_login,
                                                'user_info': user_info,
                                                })


def category(req, category_id):
    is_login = req.session.get('is_login')
    user_info = req.session.get('user_info')
    articles_obj = models.Articles.objects.filter(category_id=category_id).order_by('-ctime')
    posts = paginator(req, articles_obj)
    category_boj = models.ArticlesCategory.objects.all()
    return render(req, 'news/news_index.html', {'posts': posts,
                                                'hot_articles_obj': hot_articles_obj,
                                                'category_boj': category_boj,
                                                'is_login': is_login,
                                                'user_info': user_info,
                                                'category_id': int(category_id)}, )


def author(req, author_id):
    is_login = req.session.get('is_login')
    user_info = req.session.get('user_info')
    articles_obj = models.Articles.objects.filter(author_id=author_id).order_by('-ctime')
    posts = paginator(req, articles_obj)
    author_obj = models.Author.objects.filter(id=author_id).first()
    return render(req, 'news/news_author.html', {'posts': posts,
                                                 'hot_articles_obj': hot_articles_obj,
                                                 'is_login': is_login,
                                                 'user_info': user_info,
                                                 'author_obj': author_obj})


def article(req, category_id, article_id):
    is_login = req.session.get('is_login')
    user_info = req.session.get('user_info')
    article_obj = models.Articles.objects.filter(id=article_id).select_related('articlesdetails').first()
    articles_obj = models.Articles.objects.order_by('-ctime')[0:4]
    article_obj.views += 1
    article_obj.save()

    return render(req, 'news/news_article.html', {'post': article_obj,
                                                  'is_login': is_login,
                                                  'articles_obj': articles_obj,
                                                  'user_info': user_info,
                                                  'hot_articles_obj': hot_articles_obj,
                                                  })
