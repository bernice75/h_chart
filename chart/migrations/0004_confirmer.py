import csv
import os
from django.db import migrations
from django.conf import settings

Date = 0
China = 1
France = 2
Germany = 3
Korea_South = 4
US =  5
United_Kingdom = 6

def add_covid1(apps, schema_editor):
    Covid_confirmer = apps.get_model('chart', 'Covid19_1')  # (app_label, model_name)
    csv_file = os.path.join(settings.BASE_DIR, 'covid1.csv')
    with open(csv_file) as dataset:                   # 파일 객체 dataset
        reader = csv.reader(dataset)                    # 파일 객체 dataset에 대한 판독기 획득
        next(reader)  # ignore first row (headers)      # __next__() 호출 때마다 한 라인 판독
        for entry in reader:                            # 판독기에 대하여 반복 처리
            Covid_confirmer.objects.create(                       # DB 행 생성
                Date = entry[Date],
	            Korea_South = entry[Korea_South],
                Germany = entry[Germany],
                United_Kingdom = entry[United_Kingdom],
                US = entry[US],
                France = entry[France],
                China = entry[China]
            )

class Migration(migrations.Migration):
    dependencies = [                            # 선행 관계
        ('chart', '0003_covid19_1'),              # app_label, preceding migration file
    ]
    operations = [                              # 작업
        migrations.RunPython(add_covid1),   # add_passengers 함수를 호출
    ]