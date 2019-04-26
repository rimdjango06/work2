from django.urls import path, register_converter
from shop import views, converters

app_name = 'shop'

register_converter(converters.FourDigitYearConverter, 'yyyy')

urlpatterns = [
    path('excel/', views.response_excel),
    path('image/', views.response_image),
    path('mysum/<int:x>/<int:y>/', views.my_sum), # 뭔지 모를 int는 x로 뭔지 모를 int는 y
    path('archives/<yyyy:year>/', views.year_archive),
    path('', views.item_list),
    path('test_templates/', views.test_templates),  # 추가
]

