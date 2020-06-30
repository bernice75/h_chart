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

def add_sum(apps, schema_editor):
    Sum_Covid = apps.get_model('chart', 'Sum_covid')
    csv_file = os.path.join(settings.BASE_DIR, 'sum.csv')
    with open(csv_file) as dataset:
        reader = csv.reader(dataset)
        next(reader)
        for entry in reader:
            Sum_Covid.objects.create(
                Date=entry[Date],
                France=entry[France],
                Germany=entry[Germany],
                Korea_South=entry[Korea_South],
                US=entry[US],
                United_Kingdom=entry[United_Kingdom]
            )

class Migration(migrations.Migration):
    dependencies = [                            # 선행 관계
        ('chart', '0009_sum_covid'),              # app_label, preceding migration file
    ]
    operations = [                              # 작업
        migrations.RunPython(add_sum),   # add_passengers 함수를 호출
    ]