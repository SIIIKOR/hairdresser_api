from datetime import datetime

from django.contrib.auth.models import User
from django.db.models import ExpressionWrapper, F, DateTimeField, Q
from hairdressers import models

user = User.objects.get(pk=1)
hairdresser = models.Hairdresser.objects.get(pk=1)

start_time_str = '2022-07-12 17:30:00.000001 +00:00'
end_time_str = '2022-07-12 18:30:00.000000 +00:00'

start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S.%f %z')
end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S.%f %z')

print(
    models.Order.objects.filter(
        user=user,
        hairdresser=hairdresser
    ).annotate(
        end_time = ExpressionWrapper(
            F('start_time')+F('service__estimated_time'), 
            output_field=DateTimeField()
        )
    ).filter(
        Q(start_time__range=(start_time, end_time))|
        Q(end_time__range=(start_time, end_time))
    ).count()
)