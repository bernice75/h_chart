from django.http import JsonResponse
from django.shortcuts import render
from .models import Passenger, Covid19_1
import json
from django.db.models import Count, Q, Sum


# Create your views here.

def home(request):
    return render(request, 'home.html')

def ticket_class_view(request):
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
        'yAxis': [{'labels': {'format': '{value} %', 'style': {'color': 'blue'}}, 'title': {'text': '생존율', 'style': {'color': 'blue'}}}
            ,{'labels': {'format': '{value} 명'}, 'style': {'color': 'black'}, 'opposite': 'true', 'title': {'text': '인원', 'style': {'color': 'black'}}}],
        'tooltip': {'shared': 'true'},
        'legend': {'layout': 'vertical', 'align': 'left', 'x': 120, 'verticalAlign': 'top', 'y': 100, 'floating': 'true'},
        'series': [survived_series, not_survived_series, survived_rate]
    }
    dump = json.dumps(chart)

    return render(request, 'ticket_class.html', {'chart': dump})

def covid1(request):
    china = Covid19_1.objects.values('China').annotate(china_count=Count('China')).order_by('date')
    france = Covid19_1.objects.values('France').annotate(france_count=Count('France')).order_by('date')
    germany = Covid19_1.objects.values('Germany').annotate(germany_count=Count('Germany')).order_by('date')
    korea_South = Covid19_1.objects.values('Korea_South').annotate(korea_South_count=Count('Korea_South')).order_by('date')
    us = Covid19_1.objects.values('US').annotate(us_count=Count('US')).order_by('date')
    united_kingdom = Covid19_1.objects.values('United_Kingdom').annotate(united_kingdom_count=Count('United_Kingdom')).order_by('date')


    china_data = list()
    france_data = list()
    germany_data = list()
    korea_South_data = list()
    us_data = list()
    united_kingdom_data = list()
    date = list()


    for entry in date:
        date.append(entry['date'])
    for entry in china:
        china_data.append(entry['china_count'])
    for entry in france:
        france_data.append(entry['france_count'])
    for entry in germany:
        germany_data.append(entry['germany_count'])
    for entry in korea_South:
        korea_South_data.append(entry['korea_South_count'])
    for entry in us:
        us_data.append(entry['us_count'])
    for entry in united_kingdom:
        united_kingdom_data.append(entry['united_kingdom_count'])

    china_rate = {
        'name': 'China',
        'data': china_data,
        'color': '#089099'
    }
    france_rate = {
        'name': 'France',
        'data': france_data,
        'color': '#7CCBA2'
    }
    germany_rate = {
        'name': 'Germany',
        'data': germany_data,
        'color': '#FCDE74'
    }
    korea_South_rate = {
        'name': 'Korea, South',
        'data': korea_South_data,
        'color': '#045275'
    }
    us_rate = {
        'name': 'US',
        'data': us_data,
        'color': '#DC3977'
    }
    united_kingdom_rate = {
        'name': 'United Kingdom',
        'data': united_kingdom_data,
        'color': '#7C1D6F'
    }

    chart = {
        'chart': {'type': 'spline'},
        'title': {'text': '국가별 COVID-19 확진자 발생율'},
        'subtitle': {'text': 'Source: Johns Hopkins University Center for Systems Science and Engineering'},
        'xAxis': {'date': date, 'type': 'datetime'},
        'yAxis': {'labels': {'format': '{value} 건/백만명', 'style': {'color': 'blue'}},
               'title': {'text': '# of Cases per 1,000,000 People', 'style': {'color': 'blue'}}},
        'tooltip': {'shared': 'true'},
        'plotOptions': {'spline': {'lineWidth': 3, 'states': {'hover': {'lineWidth': 5}}}},
        'series': [china_rate, france_rate, germany_rate, korea_South_rate, us_rate, united_kingdom_rate]
    }
    dump = json.dumps(chart)

    return render(request, 'covid1.html', {'chart': dump})