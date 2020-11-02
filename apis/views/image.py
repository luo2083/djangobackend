import hashlib
import os
from django.http import JsonResponse, Http404, FileResponse
from django.views import View
from backend import settings
from utils.response import ReturnCode, CommonResponseMixin

def image(request):
    if request.method == "GET":
        md5 = request.GET.get('md5')
        imgfile = os.path.join(settings.IMAGES_DIR, md5 + '.jpg')
        if not os.path.exists(imgfile):
            return Http404()
        else:
            data = open(imgfile, 'rb').read()
            #return HttpResponse(content=data, content_type='image/jpg')
            return FileResponse(open(imgfile, 'rb'), content_type='image/jpg')

class ImageListView(View, CommonResponseMixin):
    def get(self, request):
        image_files = os.listdir(settings.IMAGES_DIR)
        response_data = []
        for image_file in image_files:
            response_data.append({
                "name": image_file,
                "md5": image_file[:-4]
            })
        data = self.wrap_json_response(data=response_data)
        print("data:", data)
        return JsonResponse(data=data, safe=False)


class ImageView(View, CommonResponseMixin):
    def get(self, request):
        md5 = request.GET.get('md5')
        imgfile = os.path.join(settings.IMAGES_DIR, md5 + '.jpg')
        if os.path.exists(imgfile):
            data = open(imgfile, 'rb').read()
            # return HttpResponse(content=data, content_type='image/jpg')
            return FileResponse(open(imgfile, 'rb'), content_type='image/jpg')
        else:
            response_data = self.wrap_json_response(code=ReturnCode.RESOURCES_NOT_EXISTS)
            return JsonResponse(data=response_data, safe=False)
    def post(self, request):
        files = request.FILES
        response = []
        for key, value in files.items():
            content = value.read()
            md5 = hashlib.md5(content).hexdigest()
            path = os.path.join(settings.IMAGES_DIR, md5 + '.jpg')
            with open(path, 'wb') as f:
                f.write(content)
                response.append({
                    "name": key,
                    "md5": md5
                })
        message = "post method success"
        response_data = self.wrap_json_response(data=response, code=ReturnCode.SUCCESS, message=message)
        return JsonResponse(data=response_data,safe=False)

    def put(self, request):
        message = "put method success"
        response_data = self.wrap_json_response(message=message)
        return JsonResponse(data=response_data,safe=False)

    def delete(self, request):
        md5 = request.GET.get('md5')
        imagename = md5 + '.jpg'
        path = os.path.join(settings.IMAGES_DIR, imagename)
        if os.path.exists(path):
            os.remove(path)
            message = "remove success"
        else:
            message = "file (%s) not found." % imagename

        response_data = self.wrap_json_response(message=message)
        return JsonResponse(data=response_data,safe=False)


