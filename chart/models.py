from django.db import models

# Create your models here.

class Passenger(models.Model):  # 승객 모델
    # 성별 상수 정의
    MALE = 'M'
    FEMALE = 'F'
    SEX_CHOICES = (
        (MALE, 'male'),
        (FEMALE, 'female')
    )

    # 승선_항구 상수 정의
    CHERBOURG = 'C' # 항구1
    QUEENSTOWN = 'Q' # 항구2
    SOUTHAMPTON = 'S' # 항구3
    PORT_CHOICES = (
        (CHERBOURG, 'Cherbourg'),
        (QUEENSTOWN, 'Queenstown'),
        (SOUTHAMPTON, 'Southampton'),
    )
    # 이 부분이 실제 테이블에 존재하는 내용들임
    name = models.CharField(max_length=100, blank=True)                 # 이름
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)           # 성별
    survived = models.BooleanField()                                    # 생존_여부
    age = models.FloatField(null=True)                                  # 연령
    ticket_class = models.PositiveSmallIntegerField()                   # 티켓_등급
    embarked = models.CharField(max_length=1, choices=PORT_CHOICES)     # 승선_항구

    def __str__(self):
        return self.name

class Covid19(models.Model) :
    country = models.CharField(max_length=100, blank=True)              # 나라
    date = models.DateTimeField()                                       # 날짜
    percapita = models.FloatField(null=True)                            #