from django.shortcuts import render
from shop.models import Item
import requests
from PIL import Image, ImageDraw, ImageFont
import pandas as pd                           # 엑셀 요청 처리
from io import BytesIO
from urllib.parse import quote
from django.http import HttpResponse

# def response_excel(request):                  # 엑셀 요청 처리
#     df = pd.DataFrame([
#         [100, 110, 120],
#         [200, 210, 220],
#     ])
#
#     io = BytesIO()
#     df.to_excel(io)
#     io.seek(0)
#
#     encoded_filename = quote('pandas.xlsx')     # '.xls'가 아니라 '.xlsx'
#     response = HttpResponse(io, content_type='application/vnd.ms-excel')
#     response['Content-Disposition'] = \
#         "attachment; filename*=utf-8''{}".format(encoded_filename)
#     return response
#
#
#
# def response_image(request):                 # 이미지 요청 처리
#    ttf_path = 'C:/Windows/Fonts/malgun.ttf' # 윈도우, 맥: '/Library/Fonts/AppleGothic.ttf'
#
#    # 이미지 파일 다운로드 혹은 로컬 디스크 상의 이미지 직접 열기
#    image_url = 'http://www.flowermeaning.com/flower-pics/Calla-Lily-Meaning.jpg'
#    res = requests.get(image_url) # 서버로 HTTP GET 요청하여, 응답 획득
#    io = BytesIO(res.content) # 응답의 Raw Body 메모리 파일 객체 BytesIO 인스턴스 생성
#    io.seek(0) # 파일의 처음으로 커서를 이동
#
#    canvas = Image.open(io).convert('RGBA') # 이미지 파일을 열고, RGBA 모드로 변환
#    font = ImageFont.truetype(ttf_path, 40) # 지정 경로의 TrueType 폰트, 폰트 크기40
#    draw = ImageDraw.Draw(canvas) # canvas에 대한 ImageDraw 객체 획득
#
#    text = 'Smart IT, by LeeHyerim'
#    left, top = 300, 300
#    margin = 10
#    width, height = font.getsize(text)
#    right = left + width + margin
#    bottom = top + height + margin
#    draw.rectangle((left, top, right, bottom), (255, 255, 224))
#    draw.text((300,300), text, font=font, fill=(20, 20, 20))
#
#    response = HttpResponse(content_type='image/png')
#    canvas.save(response, format='PNG') # HttpResponse의 유사 파일 객체 특성 활용
#    return response
#
# def year_archive(request, year):
#     if year is None:
#         return HttpResponse('{}년도 자료입니다.'.format(year))
#     else:
#         return HttpResponse('{}년도 자료는 없습니다.'.format(year))
#
# def my_sum(request, x, y):
#     result = x + y
#     output = '{} = {} + {}'.format(result, x, y)
#     return HttpResponse(output)

# class MyClass:
#     x = 10
#     y = 20

from django.shortcuts import render, get_object_or_404
from shop.models import Item, Tag
from .form import ItemForm  # b29)


from django.shortcuts import redirect
import re


def item_new(request, item=None):  # 인자가 추가되었음
    if request.method == 'POST':                        # 'POST' 요청이면
        form = ItemForm(request.POST, request.FILES, instance=item)    # 값을 가진 폼 생성
        if form.is_valid():         # 유효성 검사 통과하면
            item = form.save()      # ModelForm 기능을 이용해서 DB 저장
            return redirect(item)   # 저장된 item 보여주기
    else:                                               # 'POST' 요청 아니면
        form = ItemForm()                               # 빈 폼 생성

    return render(request, 'shop/item_form.html', {
        'form': form,               # form 자체만 맥락 변수로 전달
    })
    # error_list = []
    # initial = {}
    #
    # if request.method == 'POST':
    #     data = request.POST
    #     files = request.FILES
    #
    #     name = data.get('name')
    #     desc = data.get('desc')
    #     price = data.get('price')
    #     photo = files.get('photo')
    #     is_published = data.get('is_published') in (True, 't', 'True', '1')
    #
    #     # 유효성 검사
    #     if len(name) < 2:
    #         error_list.append('name을 2글자 이상 입력해주세요.')
    #
    #     if re.match(r'^[\da-zA-Z\s]+$', desc):
    #         error_list.append('한글을 입력해주세요.')
    #
    #     if not error_list:
    #         # 저장 시도
    #         if item is None:
    #             item = Item()
    #
    #         item.name = name
    #         item.desc = desc
    #         item.price = price
    #         item.is_published = is_published
    #         if photo:
    #             item.photo.save(photo.name, photo, save=False)
    #
    #         try:
    #             item.save()
    #         except Exception as e:
    #             error_list.append(e)
    #         else:
    #             # return redirect(item)  # item.get_absolute_url 호출됨
    #             return redirect('shop:item_list')
    #
    #     initial = {
    #         'name': name,
    #         'desc': desc,
    #         'price': price,
    #         'photo': photo,
    #         'is_published': is_published,
    #     }
    # else:
    #     if item is not None:
    #         initial = {
    #             'name': item.name,
    #             'desc': item.desc,
    #             'price': item.price,
    #             'photo': item.photo,
    #             'is_published': item.is_published,
    #         }
    # return render(request, 'shop/item_form.html', {
    #     'error_list': error_list,
    #     'initial': initial,
    # })



def item_list(request):
    items = Item.objects.all()
    # return render(
    #     request,                    # 요청 정보
    #     'shop/item_list.html',    # 템플릿 이름
    #     {'item_list': items})     # 템플릿에 전달할 정보를 사전형태
    # request.GET.get 객체에게 키 값이 'q'로 지정된 값을 요구해서 변수 q에 저장
    q = request.GET.get('q', '') # 키 값이 'q'로 지정된 값이 없으면 None이 반환됨
    if q:  # q가 널 아니면 qs에 filter 조건 추가
        items = items.filter(name__icontains=q)
    return render(request, 'shop/item_list.html', {
        'item_list': items,
        'q': q,
    })


def item_edit(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return item_new(request, item)


def item_remove(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.delete()
    return redirect('shop:item_list')

# def test_templates(requset):
#     from django.template import Context, Template
#     import datetime       # USE_TZ = True
#     from django.utils import timezone   # TIME_ZONE = 'Asia/Seoul'
#     from dateutil.parser import parse
#
#     # 맥락 변수 사전
#     my_dict = {'first_name': 'hyerim', 'last_name': 'Lee'}
#     my_obj = MyClass()
#     my_list = [1, 2, 3, 4]
#     my_date = datetime.datetime.now()
#     local_time = timezone.localtime()
#     my_b_date1 = datetime.date(2019, 12, 29)
#     my_b_date2 = parse('2010-12-29')
#     my_b_datetime = datetime.datetime(2010, 12, 29, 17, 34, 56)
#     my_string = '사랑하지 않으려면 떠나라. Love it or leave it.'
#
#     context = Context({'my_dict': my_dict, 'my_obj': my_obj, 'my_list': my_list,
#                        'my_date': my_date, 'local_time': local_time,
#                        'my_b_date1': my_b_date1, 'my_b_date2': my_b_date2,
#                        'my_b_datetime': my_b_datetime, 'my_string': my_string,
#                        })
#     template = Template(
#         "사전 < my_dict.last_name >: {{ my_dict.last_name }} <br/>"
#         + "객체 < my_obj.x >: {{ my_obj.x }} {{ my_obj.y }} <br/>"
#         + "리스트 < my_list.0 >: {{ my_list.0 }} {{ my_list.2 }}: {{ my_list.2 }} <br/>"
#         + "< my_dict.first_name|title >: {{ my_dict.first_name|title }} <br/>"
#         + "{% verbatim myblock %}{% now 'Y-m-d H:i:s' %}"
#         + "{% endverbatim myblock %} : {% now 'Y-m-d H:i:s' %} <br/>"
#         + "< my_date > : {{ my_date }} <br/>"
#         + "< local_time >: {{ local_time }} <br/>"
#         + "< my_b_date1 >: {{ my_b_date1 }} <br/>"
#         + "< my_b_date2 >: {{ my_b_date2 }} <br/>"
#         + "< my_b_date1|date:'SHORT_DATE_FORMAT' >: {{ my_b_date1|date:'SHORT_DATE_FORMAT' }} <br/>"
#         + "(마지막에 점이 찍힘!! 필터 내부에서 인수를 표시할 때 사용하는 \':\' 뒤에 띄우지 말 것!)<br/>"
#         + "< my_b_date1|date:'Y년 m월 d일' >: {{ my_b_date1|date:'Y년 m월 d일' }} <br/>"
#         # + "< my_b_date|date:'LONG_DATE_FORMAT' >(???)': {{ my_b_date|date:'LONG_DATE_FORMAT' }} <br/>"
#         # + "(필터 내부에서 인수를 표시할 때 사용하는 \':\' 뒤에 띄우지 말 것!)<br/>" # 오류!!
#         + "< my_b_datetime >: {{ my_b_datetime }} <br/>"
#         + "< my_b_datetime|date:'Y년 m월 d일' > < my_b_datetime|time:'H시 i분 s초' >: "
#             + "{{ my_b_datetime|date:'Y년 m월 d일' }}  {{ my_b_datetime|time:'H시 i분 s초' }} <br/>"
#             + "(필터 내부에서 인수를 표시할 때 사용하는 \':\' 뒤에 띄우지 말 것!)<br/>"
#         + "< my_string|lower|truncatewords:'4' >: {{ my_string|lower|truncatewords:'4' }} <br/>"
#             + "(필터 내부에서 인수를 표시할 때 사용하는 \':\' 뒤에 띄우지 말 것!)<br/>"
#         + "< my_string|lower|truncatechars:'12' >: {{ my_string|lower|truncatechars:'12' }} <br/>"
#             +"(필터 내부에서 인수를 표시할 때 사용하는 \':\' 뒤에 띄우지 말 것!)<br/>"
#     )
#     content = template.render(context)
#
#     return HttpResponse(content)


def item_list(request):
    qs = Item.objects.all()
    return render(request, 'shop/item_list.html',
                  {'item_list': qs})


def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    all_tag = Tag.objects.all()
    mystr = item.tagged()
    my_tag = {}
    for t in all_tag:
        # mystr에서 t.name을 발견한 위치를 my_tag 사전에 등록
        # 키는 t.name으로, 값은 (못 찾으면 -1, 찾으면 양수)
        my_tag[t.name] = str(mystr).find(t.name)
    return render(request, 'shop/item_detail.html',
                  {'item': item, 'my_tag': my_tag})

