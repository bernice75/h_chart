# Generated by Django 3.0.3 on 2020-06-15 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0002_auto_popuate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Covid19_1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('China', models.FloatField(null=True)),
                ('France', models.FloatField(null=True)),
                ('Germany', models.FloatField(null=True)),
                ('Korea_South', models.FloatField(null=True)),
                ('US', models.FloatField(null=True)),
                ('United_Kingdom', models.FloatField(null=True)),
            ],
        ),
    ]
