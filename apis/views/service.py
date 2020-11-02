import json
import os
import random
from backend import settings
from django.http import JsonResponse
from utils.response import ReturnCode, CommonResponseMixin
from utils.auth import already_authorized, get_user
from thirdparty import juhe

all_constellations = ['白羊座', '金牛座', '双子座', '巨蟹座', '狮子座', '处女座', '天秤座', '天蝎座', '射手座', '摩羯座', '水瓶座', '双鱼座']

def constellation(request):
    data = []
    if already_authorized(request):
        user = get_user(request)
        constellations = json.loads(user.focus_constellations)
    else:
        constellations = all_constellations
    for c in constellations:
        result = juhe.constellation(c)
        data.append(result)
    response_data = CommonResponseMixin.wrap_json_response(data=data, code=ReturnCode.SUCCESS)
    return JsonResponse(data=response_data, safe=False)
all_jokes = []
def joke(request):
    global all_jokes
    if not all_jokes:
        all_jokes = json.load(open(os.path.join(settings.BASE_DIR, 'jokes.json'), 'r'))
    limits = 10
    sample_jokes = random.sample(all_jokes, limits)
    response_data = CommonResponseMixin.wrap_json_response(data=sample_jokes)
    return JsonResponse(data=response_data,safe=False)