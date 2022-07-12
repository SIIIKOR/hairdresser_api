from random import randint, choice
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.utils import timezone

from hairdressers import models

YEAR = 2022
MONTH = [7]
DAYS = [i for i in range(1, 29)]
HOURS = [i for i in range(8, 16)]
MINUTES = [0, 15, 30, 45]

dates = [
    datetime(
        year=YEAR,
        month=choice(MONTH),
        day=choice(DAYS),
        hour=choice(HOURS),
        minute=choice(MINUTES),
        tzinfo=timezone.utc
    ) for _ in range(200)
]

services = []
hairdressers = []

for i in range(10):
    service = models.Service.objects.create(
        name = f"haircut{i}",
        price = randint(0, 99999)/100,
        estimated_time = timedelta(
            minutes=choice(
                [30, 45, 60, 90, 120]
            )
        )
    )
    services.append(service)

for i in range(5):
    hairdresser = models.Hairdresser.objects.create(
        name = f"hairdresser{i}",
        surname = f"surname{i}",
        email = f"hairdresser{i}@gmail.com"
    )
    hairdressers.append(hairdresser)

for i in range(40):
    user = User.objects.create_user( # type: ignore
        username=f"user{i}",
        email=f"user{i}@gmail.com",
        password=f"1234"
    )

    for i in range(randint(1, 4)):
        hairdresser = choice(hairdressers)
        service = choice(services)

        order = models.Order.objects.create(
            user=user,
            hairdresser=hairdresser,
            service=service,
            start_time=choice(dates)
        )