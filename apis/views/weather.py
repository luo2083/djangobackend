
import json
from django.http import JsonResponse
from thirdparty import juhe
from django.views import View
from authorization.models import User
from utils.auth import already_authorized
from utils.response import CommonResponseMixin, ReturnCode


class WeatherView(View, CommonResponseMixin):
    def get(self, request):
        if not already_authorized(request):
            return JsonResponse({}, code=ReturnCode.UNAUTHORIZED)
        else:
            data = []
            open_id = request.session.get('open_id')
            user = User.objects.filter(open_id=open_id)[0]
            cities = json.loads(user.focus_cities)
            for city in cities:
                result = juhe.weather(city.get('city'))
                result['city_info'] = city
                data.append(result)
            response = self.wrap_json_response(data=data, code=ReturnCode.SUCCESS)
        return JsonResponse(data=response, safe=False)
    def post(self, request):
        data = []
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        print(received_body)
        cities = received_body.get('cities')
        for city in cities:
            result = juhe.weather(city.get('city'))
            result['city'] = city.get('city')
            result['province'] = city.get('province')
            data.append(result)
        response_data = self.wrap_json_response(data=data)
        print(response_data)
        return JsonResponse(data=response_data, safe=False)

