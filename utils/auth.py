import json
import requests
from utils import proxy
import backend.settings
from authorization.models import User

from authorization.models import User

def already_authorized(request):
    is_authorized = False
    if request.session.get('is_authorized'):
        is_authorized = True
    return is_authorized
def get_user(request):
    if not already_authorized(request):
        raise Exception('not authorized request')
    open_id = request.session.get('open_id')
    user = User.objects.get(open_id=open_id)
    return user
def c2s(appid, code):
    return code2session(appid, code)

def code2session(appid, code):
    API = 'https://api.weixin.qq.com/sns/jscode2session'
    params = 'appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' %(appid, backend.settings.WX_APP_SECRET, code)
    url = API + '?' + params
    response_data = requests.get(url, proxies=proxy.proxy())
    data = json.loads(response_data.text)
    print(data)
    return data