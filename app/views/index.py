from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from app import forms
from reposition import models, model_query, model_update, model_add
from utils.check_code import create_validate_code
import io
import datetime
from utils.menu import get_cate_dic

def index(req):
    is_login = None
    if req.method == 'GET':
        bxSlider = models.Bxslider.objects.filter(status=1).order_by('weight').all()
        cate_dic = get_cate_dic()
        cookie = req.COOKIES
        is_login = req.session.get('is_login')

        return render(req, 'index.html', {'bxSlider': bxSlider, 'cate_dic': cate_dic,
                                          'cookie': cookie, 'is_login': is_login,})
