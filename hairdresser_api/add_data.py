from random import randint, choice
from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone

from hairdressers.models import Service, Hairdresser, Order

for i in range(100):
    user = User.objects.create_user( # type: ignore
        username=f"user{i}",
        email=f"user{i}@gmail.com",
        password=f"1234"
    )
    service = Service.objects.create(
        name = f"haircut{i}",
        price = randint(0, 99999)/100,
        estimated_time = timedelta(
            minutes=choice(
                [30, 45, 60, 90, 120]
            )
        )
    )
    hairdresser = Hairdresser.objects.create(
        name = f"hairdresser{i}",
        surname = f"surname{i}",
        email = f"hairdresser{i}@gmail.com"
    )
    order = Order.objects.create(
        customer=user,
        hairdresser=hairdresser,
        service=service,
        start_time=timezone.now()
    )