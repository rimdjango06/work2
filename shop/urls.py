from django.urls import path, register_converter
from shop import views, converters

app_name = 'shop'

# register_converter(converters.FourDigitYearConverter, 'yyyy')

urlpatterns = [
    # path('excel/', views.response_excel),
    # path('image/', views.response_image),
    # path('mysum/<int:x>/<int:y>/', views.my_sum), # 뭔지 모를 int는 x로 뭔지 모를 int는 y
    # path('archives/<yyyy:year>/', views.year_archive),
    path('', views.item_list, name='item_list'),                     # 조회
    path('view/<int:pk>/', views.item_detail, name='item_detail'),   # 조회
    path('new/', views.item_new, name='item_new'),                   # 등록
    path('remove/<int:pk>/', views.item_remove, name='item_remove'), # 삭제
    path('edit/<int:pk>/', views.item_edit, name='item_edit'),       # 수정
    # path('test_templates/', views.test_templates),  # 추가
]

