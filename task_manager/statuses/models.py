from django.db import models


class Status(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Имя'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return self.name
