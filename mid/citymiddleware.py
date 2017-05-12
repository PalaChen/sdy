from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from reposition import models


class CityMid(MiddlewareMixin):
    def process_request(self, request, *args, **kwargs):
        session_dict = request.session
        # print(request.COOKIES)
        # city_obj = models.RegionalManagement.objects.filter(name='佛山市').first()
        # area_obj = models.RegionalManagement.objects.filter(name='顺德区').first()
        # HttpResponse
        # print(request.COOKIES)
        if not session_dict.get('default_city'):
            city_obj = models.RegionalManagement.objects.filter(name='佛山市').first()
            area_obj = models.RegionalManagement.objects.filter(name='顺德区').first()
            request.session['default_city'] = {'city_id': city_obj.id, 'city': city_obj.name, 'area_id': area_obj.id}
        print(request.session['default_city'])
        # def process_response(self, request, *args, **kwargs):
        #     pass
