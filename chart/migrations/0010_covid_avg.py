import csv
import os
from django.db import migrations
from django.conf import settings
# Date,France,Germany,"Korea, South",US,United Kingdom
Date = 0
Korea_South = 3
Germany = 2
United_Kingdom = 5
US =  4
France = 1

def add_avg(apps, schema_editor):
    Percapita = apps.get_model('chart', 'Percapita')
    csv_file = os.path.join(settings.BASE_DIR, 'percapita.csv')
    with open(csv_file) as dataset:
        reader = csv.reader(dataset)
        next(reader)
        for entry in reader:
            Percapita.objects.create(
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
        migrations.RunPython(add_avg),   # add_passengers 함수를 호출
    ]