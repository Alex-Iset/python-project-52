from django.db import models

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import User


class Task(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Имя'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='tasks',
        verbose_name='Статус'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='tasks_created',
        verbose_name='Автор'
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='tasks_assigned',
        verbose_name='Исполнитель'
    )
    labels = models.ManyToManyField(
        Label,
        blank=True,
        related_name='tasks',
        verbose_name='Метки'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return self.name