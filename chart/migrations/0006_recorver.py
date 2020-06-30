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

def add_recorver(apps, schema_editor):
    Recorver = apps.get_model('chart', 'Covid19_re')
    csv_file = os.path.join(settings.BASE_DIR, 'recorver.csv')
    with open(csv_file) as dataset:
        reader = csv.reader(dataset)
        next(reader)
        for entry in reader:
            Recorver.objects.create(
                Date=entry[Date],
                France=entry[France],
                Germany=entry[Germany],
                Korea_South=entry[Korea_South],
                US=entry[US],
                United_Kingdom=entry[United_Kingdom]
            )

class Migration(migrations.Migration):
    dependencies = [                            # 선행 관계
        ('chart', '0005_covid19_re'),              # app_label, preceding migration file
    ]
    operations = [                              # 작업
        migrations.RunPython(add_recorver),   # add_passengers 함수를 호출
    ]