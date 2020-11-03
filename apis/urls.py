
from django.urls import path

from .views import weather, menu, image, service,test


urlpatterns = [
    #path('', weather.helloworld)
    #path('', weather.weather)
    path('weather', weather.WeatherView.as_view()),
    path('menu', menu.get_menu),
    #path('image',image.image),
    #path('imagetext', image.image_text)
    path('image', image.ImageView.as_view()),
    path('image/list', image.ImageListView.as_view()),
    path('constellation', service.constellation),
    path('joke', service.joke),
    path('test', test.test),
]