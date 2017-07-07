from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_delete = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    @classmethod
    def remove(cls, id):
        obj = cls.objects.get(id=id)
        obj.is_delete = True
        obj.save()
