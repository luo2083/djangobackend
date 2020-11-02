import json
from django.http import JsonResponse
from django.views import View
from utils.auth import c2s, already_authorized
from utils.response import CommonResponseMixin, ReturnCode
from authorization.models import User

def test_session(request):
    request.session['message'] = 'Test session ok'
    response_data = CommonResponseMixin.wrap_json_response(code=ReturnCode.SUCCESS)
    return JsonResponse(data=response_data, safe=False)
class UserView(View, CommonResponseMixin):
    def get(self, request):
        if not already_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.SUCCESS)
            return JsonResponse(data=response, safe=False)
        open_id = request.session.get('open_id')
        user = User.objects.get(open_id=open_id)
        data = {}
        data['open_id'] = user.open_id
        data['focus'] = {}
        print(user.focus_cities)
        data['focus']['city'] = json.loads(user.focus_cities)
        data['focus']['constellation'] = json.loads(user.focus_constellations)
        print('data: ', data)
        response = self.wrap_json_response(data=data, code=ReturnCode.SUCCESS)
        print('response is :',response)
        return JsonResponse(data=response, safe=False)

    def post(self, request):
        if not already_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.SUCCESS)
            return JsonResponse(data=response, safe=False)
        open_id = request.session.get('open_id')
        user = User.objects.get(open_id=open_id)

        received_body = request.body.decode('utf-8')
        received_body = eval(received_body)
        cities = received_body.get('city')
        constellations = received_body.get('constellation')
        user.focus_cities = json.dumps(cities)
        user.focus_constellations = json.dumps(constellations)
        user.save()

        response = self.wrap_json_response(code=ReturnCode.SUCCESS, message='modify user info success.')
        return JsonResponse(data=response, safe=False)

def __authorize_by_code(request):
    post_data = request.body.decode('utf-8')
    post_data = json.loads(post_data)
    code = post_data.get('code').strip()
    app_id = post_data.get('appId').strip()
    nickname = post_data.get('nickname').strip()

    response_data = {}
    if not code or not app_id:
        response_data['message'] = 'authorized failed, need entire authorization data.'
        response_data['code'] = ReturnCode.BROKEN_AUTHORIZED_DATA
        return JsonResponse(data=response_data, safe=False)

    data = c2s(app_id, code)
    openid = data.get('openid')
    print('get openid:', openid)

    if not openid:
        response = CommonResponseMixin.wrap_json_response(code=ReturnCode.FAILED, message='auth failed')
        return JsonResponse(data=response, safe=False)
    request.session['open_id'] = openid
    request.session['is_authorized'] = True

    if not User.objects.filter(open_id=openid):
        new_user = User(open_id=openid, nickname=nickname)
        print('new_user:open_id:%s, nickname:%s' %(openid, nickname))
        new_user.save()
    response = CommonResponseMixin.wrap_json_response(code=ReturnCode.SUCCESS, message='auth succeess')
    return JsonResponse(data=response, safe=False)

def get_status(request):
    print('call get_status function....')
    if already_authorized(request):
        data = {"is_authorized": 1}
    else:
        data = {"is_authorized": 0}
    response = CommonResponseMixin.wrap_json_response(data=data, code=ReturnCode.SUCCESS)
    return JsonResponse(data=response, safe=False)

def logout(request):
    request.session.clear()
    response = {}
    response['result_code'] = 0
    response['message'] = 'logout success.'
    return JsonResponse(response, safe=False)

def authorize(request):
    return __authorize_by_code(request)

def test_session2(request):
    print('session content: ', request.session.items())
    response = CommonResponseMixin.wrap_json_response(code=ReturnCode.SUCCESS)
    return JsonResponse(data=response, safe=False)


