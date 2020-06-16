import csv
import os
from django.db import migrations
from django.conf import settings
# Date,France,Germany,"Korea, South",US,United Kingdom
Date = 0
France = 1
Germany = 2
Korea_South = 3
US =  4
United_Kingdom = 5

def add_percapita(apps, schema_editor):
    Covid_Percapita = apps.get_model('chart', 'Percapita')  # (app_label, model_name)
    csv_file = os.path.join(settings.BASE_DIR, 'percapita.csv')
    with open(csv_file) as dataset:                   # 파일 객체 dataset
        reader = csv.reader(dataset)                    # 파일 객체 dataset에 대한 판독기 획득
        next(reader)  # ignore first row (headers)      # __next__() 호출 때마다 한 라인 판독
        for entry in reader:                            # 판독기에 대하여 반복 처리
            Covid_Percapita.objects.create(                       # DB 행 생성
                Date=entry[Date],
                Korea_South=entry[Korea_South],
                Germany=entry[Germany],
                United_Kingdom=entry[United_Kingdom],
                US=entry[US],
                France=entry[France]
            )

class Migration(migrations.Migration):
    dependencies = [                            # 선행 관계
        ('chart', '0009_percapita'),              # app_label, preceding migration file
    ]
    operations = [                              # 작업
        migrations.RunPython(add_percapita),   # add_passengers 함수를 호출
    ]