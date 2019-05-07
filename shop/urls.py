from django.urls import path, register_converter
from shop import views

app_name = 'shop'

# register_converter(converters.FourDigitYearConverter, 'yyyy')

urlpatterns = [
    # path('excel/', views.response_excel),
    # path('image/', views.response_image),
    # path('mysum/<int:x>/<int:y>/', views.my_sum), # 뭔지 모를 int는 x로 뭔지 모를 int는 y
    # path('archives/<yyyy:year>/', views.year_archive),
    path('', views.item_list, name='item_detail'),
    path('<int:pk>/', views.item_detail, name='item_detail'),
    # path('test_templates/', views.test_templates),  # 추가
]

