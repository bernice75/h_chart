from django.http import JsonResponse
from django.shortcuts import render
from .models import Passenger, Covid19_1, Covid19_2, Covid19_3
import json
import arrow
from django.db.models import Count, Q


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
    survived_rate_data = list()

    # 리스트 3종에 형식화된 값을 등록
    for entry in dataset:
        categories.append('%s 등석' % entry['ticket_class'])  # for xAxis
        survived_series_data.append(entry['survived_count'])  # for series named 'Survived'
        not_survived_series_data.append(entry['not_survived_count'])  # for series named 'Not survived'
        survived_rate_data.append(entry['survived_count'] / (entry['survived_count']+entry['not_survived_count']) * 100)

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
        'data': survived_rate_data,
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
    korea_South = Covid19_1.objects.values('Korea_South').order_by('Date')
    germany = Covid19_1.objects.values('Germany').order_by('Date')
    united_kingdom = Covid19_1.objects.values('United_Kingdom').order_by('Date')
    us = Covid19_1.objects.values('US').order_by('Date')
    france = Covid19_1.objects.values('France').order_by('Date')
    china = Covid19_1.objects.values('China').order_by('Date')

    date_data = list()
    korea_South_data = list()
    germany_data = list()
    united_kingdom_data = list()
    us_data = list()
    france_data = list()
    china_data = list()


    for entry in date_data:
        date_data.append(entry['Date'])
    for entry in korea_South:
        korea_South_data.append(entry['Korea_South'])
    for entry in germany:
        germany_data.append(entry['Germany'])
    for entry in united_kingdom:
        united_kingdom_data.append(entry['United_Kingdom'])
    for entry in us:
        us_data.append(entry['US'])
    for entry in france:
        france_data.append(entry['France'])
    for entry in china:
        china_data.append(entry['China'])

    korea_South_rate = {
        'name': 'Korea, South',
        'data': china_data,
        'pointInterval': 24 * 3600 * 1200,
        'color': '#045275'
    }
    germany_rate = {
        'name': 'Germany',
        'data': france_data,
        'pointInterval': 24 * 3600 * 1200,
        'color': '#FCDE74'
    }
    united_kingdom_rate = {
        'name': 'United Kingdom',
        'data': germany_data,
        'pointInterval': 24 * 3600 * 1200,
        'color': '#7C1D6F'
    }
    us_rate = {
        'name': 'US',
        'data': united_kingdom_data,
        'pointInterval': 24 * 3600 * 1200,
        'color': '#DC3977'
    }
    france_rate = {
        'name': 'France',
        'data': us_data,
        'pointInterval': 24 * 3600 * 1200,
        'color': '#7CCBA2'
    }
    china_rate = {
        'name': 'China',
        'data': korea_South_data,
        'pointInterval': 24 * 3600 * 1200,
        'color': '#089099',
    }

    chart = {
        'chart': {'type': 'spline'},
        'title': {'text': '국가별 COVID-19 확진자 발생율'},
        'subtitle': {'text': 'For the USA, China, Germany, France, United Kingdom, and Korea, South Confirmer'},
        'xAxis': {'date': date_data, 'type': 'datetime', 'labels': {'format': '{value: %d. %b}'}},
        'yAxis': {'tickInterval': 5000, 'labels': {'format': '{value} 건/백만명', 'style': {'color': 'blue'}},
               'title': {'text': '# of Cases per 1,000,000 People', 'style': {'color': 'blue'}}},
        'plotOptions': {'spline': {'lineWidth': 3, 'states': {'hover': {'lineWidth': 5}}}},
        'series': [china_rate, france_rate, germany_rate, korea_South_rate, us_rate, united_kingdom_rate],
        'navigation': {'menuItemStyle': {'fontSize': '10px'}}
    }
    dump = json.dumps(chart)

    return render(request, 'covid1.html', {'chart': dump})

def covid2(request):
    korea_South = Covid19_2.objects.values('Korea_South').order_by('Date')
    germany = Covid19_2.objects.values('Germany').order_by('Date')
    united_kingdom = Covid19_2.objects.values('United_Kingdom').order_by('Date')
    us = Covid19_2.objects.values('US').order_by('Date')
    france = Covid19_2.objects.values('France').order_by('Date')
    china = Covid19_2.objects.values('China').order_by('Date')

    date_data = list()
    korea_South_data = list()
    germany_data = list()
    united_kingdom_data = list()
    us_data = list()
    france_data = list()
    china_data = list()


    for entry in date_data:
        date_data.append(entry['Date'])
    for entry in korea_South:
        korea_South_data.append(entry['Korea_South'])
    for entry in germany:
        germany_data.append(entry['Germany'])
    for entry in united_kingdom:
        united_kingdom_data.append(entry['United_Kingdom'])
    for entry in us:
        us_data.append(entry['US'])
    for entry in france:
        france_data.append(entry['France'])
    for entry in china:
        china_data.append(entry['China'])

    korea_South_rate = {
        'name': 'Korea, South',
        'data': china_data,
        'pointInterval': 24 * 3600 * 1200,
        'color': '#045275'
    }
    germany_rate = {
        'name': 'Germany',
        'data': france_data,
        'pointInterval': 24 * 3600 * 1200,
        'color': '#FCDE74'
    }
    united_kingdom_rate = {
        'name': 'United Kingdom',
        'data': germany_data,
        'pointInterval': 24 * 3600 * 1200,
        'color': '#7C1D6F'
    }
    us_rate = {
        'name': 'US',
        'data': united_kingdom_data,
        'pointInterval': 24 * 3600 * 1200,
        'color': '#DC3977'
    }
    france_rate = {
        'name': 'France',
        'data': us_data,
        'pointInterval': 24 * 3600 * 1200,
        'color': '#7CCBA2'
    }
    china_rate = {
        'name': 'China',
        'data': korea_South_data,
        'pointInterval': 24 * 3600 * 1200,
        'color': '#089099',
    }

    chart = {
        'chart': {'type': 'spline'},
        'title': {'text': '국가별 COVID-19 회복자 발생율'},
        'subtitle': {'text': 'For the USA, China, Germany, France, United Kingdom, and Korea, South Confirmer'},
        'xAxis': {'date': date_data, 'type': 'datetime', 'labels': {'format': '{value: %d. %b}'}},
        'yAxis': {'tickInterval': 2000, 'labels': {'format': '{value} 건/백만명', 'style': {'color': 'blue'}},
               'title': {'text': '# of Cases per 1,000,000 People', 'style': {'color': 'blue'}}},
        'plotOptions': {'spline': {'lineWidth': 3, 'states': {'hover': {'lineWidth': 5}}}},
        'series': [china_rate, france_rate, germany_rate, korea_South_rate, us_rate, united_kingdom_rate],
        'navigation': {'menuItemStyle': {'fontSize': '10px'}}
    }
    dump = json.dumps(chart)

    return render(request, 'covid2.html', {'chart': dump})

def covid3(request):
    korea_South = Covid19_3.objects.values('Korea_South').order_by('Date')
    germany = Covid19_3.objects.values('Germany').order_by('Date')
    united_kingdom = Covid19_3.objects.values('United_Kingdom').order_by('Date')
    us = Covid19_3.objects.values('US').order_by('Date')
    france = Covid19_3.objects.values('France').order_by('Date')
    china = Covid19_3.objects.values('China').order_by('Date')

    date_data = list()
    korea_South_data = list()
    germany_data = list()
    united_kingdom_data = list()
    us_data = list()
    france_data = list()
    china_data = list()


    for entry in date_data:
        date_data.append(entry['Date'])
    for entry in korea_South:
        korea_South_data.append(entry['Korea_South'])
    for entry in germany:
        germany_data.append(entry['Germany'])
    for entry in united_kingdom:
        united_kingdom_data.append(entry['United_Kingdom'])
    for entry in us:
        us_data.append(entry['US'])
    for entry in france:
        france_data.append(entry['France'])
    for entry in china:
        china_data.append(entry['China'])

    korea_South_rate = {
        'name': 'Korea, South',
        'data': china_data,
        'pointInterval': 24 * 3600 * 1200,
        'color': '#045275'
    }
    germany_rate = {
        'name': 'Germany',
        'data': france_data,
        'pointInterval': 24 * 3600 * 1200,
        'color': '#FCDE74'
    }
    united_kingdom_rate = {
        'name': 'United Kingdom',
        'data': germany_data,
        'pointInterval': 24 * 3600 * 1200,
        'color': '#7C1D6F'
    }
    us_rate = {
        'name': 'US',
        'data': united_kingdom_data,
        'pointInterval': 24 * 3600 * 1200,
        'color': '#DC3977'
    }
    france_rate = {
        'name': 'France',
        'data': us_data,
        'pointInterval': 24 * 3600 * 1200,
        'color': '#7CCBA2'
    }
    china_rate = {
        'name': 'China',
        'data': korea_South_data,
        'pointInterval': 24 * 3600 * 1200,
        'color': '#089099',
    }

    chart = {
        'chart': {'type': 'spline'},
        'title': {'text': '국가별 COVID-19 회복자 발생율'},
        'subtitle': {'text': 'For the USA, China, Germany, France, United Kingdom, and Korea, South Confirmer'},
        'xAxis': {'date': date_data, 'type': 'datetime', 'labels': {'format': '{value: %d. %b}'}},
        'yAxis': {'tickInterval': 250, 'labels': {'format': '{value} 건/백만명', 'style': {'color': 'blue'}},
               'title': {'text': '# of Cases per 1,000,000 People', 'style': {'color': 'blue'}}},
        'plotOptions': {'spline': {'lineWidth': 3, 'states': {'hover': {'lineWidth': 5}}}},
        'series': [china_rate, france_rate, germany_rate, korea_South_rate, us_rate, united_kingdom_rate],
        'navigation': {'menuItemStyle': {'fontSize': '10px'}}
    }
    dump = json.dumps(chart)

    return render(request, 'covid3.html', {'chart': dump})