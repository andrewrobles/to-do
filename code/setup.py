import json
from django.contrib.auth.models import User

if User.objects.count() == 0:
    username = 'admin'
    password = '1234'
    email = 'admin@example.com'

    user = User(
        username=username,
        email=email
    )

    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True

    user.save()