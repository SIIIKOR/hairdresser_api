from random import randint, choice
from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone

from rest_framework.authtoken.models import Token

from hairdressers import models


for i in range(40):
    user = User.objects.create_user( # type: ignore
        username=f"user{i}",
        email=f"user{i}@gmail.com",
        password=f"1234"
    )

    Token.objects.get_or_create(user=user)

    service = models.Service.objects.create(
        name = f"haircut{i}",
        price = randint(0, 99999)/100,
        estimated_time = timedelta(
            minutes=choice(
                [30, 45, 60, 90, 120]
            )
        )
    )
    hairdresser = models.Hairdresser.objects.create(
        name = f"hairdresser{i}",
        surname = f"surname{i}",
        email = f"hairdresser{i}@gmail.com"
    )
    order = models.Order.objects.create(
        user=user,
        hairdresser=hairdresser,
        service=service,
        start_time=timezone.now()
    )