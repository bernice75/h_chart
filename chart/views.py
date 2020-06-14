from django.http import JsonResponse
from django.shortcuts import render
from .models import Passenger
import json
from django.db.models import Count, Q, Sum


# Create your views here.

def home(request):
    return render(request, 'home.html')

def world_population(request):
    return render(request, 'world_population.html')

def ticket_class_view_1(request):  # 방법 1
    dataset = Passenger.objects \
        .values('ticket_class') \
        .annotate(
        survived_count=Count('ticket_class', filter=Q(survived=True)),
        not_survived_count=Count('ticket_class', filter=Q(survived=False)),
        survier_rate=Sum('ticket_class', filter=Q(survived=True)) / Sum('ticket_class') * 100) \
        .order_by('ticket_class')
    return render(request, 'ticket_class_1.html', {'dataset': dataset})


 # dataset = [
 #   {'ticket_class': 1, 'survived_count': 200, 'not_survived_count': 123},
 #   {'ticket_class': 2, 'survived_count': 119, 'not_survived_count': 158},
 #   {'ticket_class': 3, 'survived_count': 181, 'not_survived_count': 528}
 # ]

def ticket_class_view_2(request):  # 방법 2
    dataset = Passenger.objects \
        .values('ticket_class') \
        .annotate(survived_count=Count('ticket_class', filter=Q(survived=True)),
                  not_survived_count=Count('ticket_class', filter=Q(survived=False))) \
        .order_by('ticket_class')

    # 빈 리스트 3종 준비
    categories = list()  # for xAxis
    survived_series = list()  # for series named 'Survived'
    not_survived_series = list()  # for series named 'Not survived'

    # 리스트 3종에 형식화된 값을 등록
    for entry in dataset:
        categories.append('%s Class' % entry['ticket_class'])  # for xAxis
        survived_series.append(entry['survived_count'])  # for series named 'Survived'
        not_survived_series.append(entry['not_survived_count'])  # for series named 'Not survived'

    # json.dumps() 함수로 리스트 3종을 JSON 데이터 형식으로 반환
    return render(request, 'ticket_class_2.html', {
        'categories': json.dumps(categories),
        'survived_series': json.dumps(survived_series),
        'not_survived_series': json.dumps(not_survived_series)
    })

def ticket_class_view_3(request):  # 방법 3
    dataset = Passenger.objects \
        .values('ticket_class') \
        .annotate(survived_count=Count('ticket_class', filter=Q(survived=True)),
                  not_survived_count=Count('ticket_class', filter=Q(survived=False))) \
        .order_by('ticket_class')

    # 빈 리스트 3종 준비 (series 이름 뒤에 '_data' 추가)
    categories = list()  # for xAxis
    survived_series_data = list()  # for series named 'Survived'
    not_survived_series_data = list()  # for series named 'Not survived'

    # 리스트 3종에 형식화된 값을 등록
    for entry in dataset:
        categories.append('%s 등석' % entry['ticket_class'])  # for xAxis
        survived_series_data.append(entry['survived_count'])  # for series named 'Survived'
        not_survived_series_data.append(entry['not_survived_count'])  # for series named 'Not survived'

    survived_series = {
        'name': '생존',
        'yAxis': 1,
        'data': survived_series_data,
        'color': 'green',
        'tooltip': {'valueSuffix': ' 명'}
    }
    not_survived_series = {
        'name': '비 생존',
        'yAxis': 1,
        'data': not_survived_series_data,
        'color': 'red',
        'tooltip': {'valueSuffix': ' 명'}
    }
    survived_rate = {
        'type': 'spline',
        'name': '생존율',
        'data': [61.91950464396285, 42.96028880866426, 25.52891396332863],
        'tooltip': {'valueSuffix': ' %'}
    }

    chart = {
        'chart': {'type': 'column', 'zoomType': 'xy'},
        'title': {'text': '좌석 등급에 따른 타이타닉 생존/비 생존 인원 및 생존율'},
        'xAxis': {'categories': categories},
        'yAxis': [{'labels': {'format': '{value} %'}, 'style': {'color': 'blue'}, 'title': {'text': '생존율', 'style': {'color': 'blue'}}}
            ,{'labels': {'format': '{value} 명'}, 'style': {'color': 'black'}, 'opposite': 'true', 'title': {'text': '인원', 'style': {'color': 'black'}}}],
        'tooltip': {'shared': 'true'},
        'legend': {'layout': 'vertical', 'align': 'left', 'x': 120, 'verticalAlign': 'top', 'y': 100, 'floating': 'true'},
        'series': [survived_series, not_survived_series, survived_rate]
    }
    dump = json.dumps(chart)

    return render(request, 'ticket_class_3.html', {'chart': dump})

def covid1(request):
    dataset = Passenger.objects \
        .values('ticket_class') \
        .annotate(
        survived_count=Count('ticket_class',
                             filter=Q(survived=True)),
        not_survived_count=Count('ticket_class',
                                 filter=Q(survived=False))) \
        .order_by('ticket_class')

    return render(request, 'covid1.html', {'dataset': dataset})

def json_example(request):  # 방법 4
    return render(request, 'json_example.html')

def chart_data(request):  # 방법 4
    dataset = Passenger.objects \
        .values('embarked') \
        .exclude(embarked='') \
        .annotate(total=Count('id')) \
        .order_by('-total')
    #  [
    #    {'embarked': 'S', 'total': 914}
    #    {'embarked': 'C', 'total': 270},
    #    {'embarked': 'Q', 'total': 123},
    #  ]

    # # 탑승_항구 상수 정의
    # CHERBOURG = 'C'
    # QUEENSTOWN = 'Q'
    # SOUTHAMPTON = 'S'
    # PORT_CHOICES = (
    #     (CHERBOURG, 'Cherbourg'),
    #     (QUEENSTOWN, 'Queenstown'),
    #     (SOUTHAMPTON, 'Southampton'),
    # )
    port_display_name = dict()
    for port_tuple in Passenger.PORT_CHOICES:
        port_display_name[port_tuple[0]] = port_tuple[1]
    # port_display_name = {'C': 'Cherbourg', 'Q': 'Queenstown', 'S': 'Southampton'}

    chart = {
        'chart': {'type': 'pie'},
        'title': {'text': 'Number of Titanic Passengers by Embarkation Port'},
        'series': [{
            'name': 'Embarkation Port',
            'data': list(map(
                lambda row: {'name': port_display_name[row['embarked']], 'y': row['total']},
                dataset))
            # 'data': [ {'name': 'Southampton', 'y': 914},
            #           {'name': 'Cherbourg', 'y': 270},
            #           {'name': 'Queenstown', 'y': 123}]
        }]
    }
    # [list(map(lambda))](https://wikidocs.net/64)

    return JsonResponse(chart)