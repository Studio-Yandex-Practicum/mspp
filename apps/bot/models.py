from django.db import models


class BaseModel(models.Model):
    """
    An abstract base class model.
    It provides self-updating ``created_at`` and ``updated_at`` fields.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.id}"


class City(BaseModel):
    """
    City class model.
    It provides ``name`` field.
    """

    name = models.CharField(
        verbose_name='Наименование',
        max_length=100,
        help_text='Название города.',
        )

    class Meta:
        ordering = ('name', )
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name


class Fund(BaseModel):
    """
    Fund class model.
    It provides ``name`` field.
    """

    name = models.CharField(
        verbose_name='Наименование',
        max_length=256,
        help_text='Название фонда.',
        )

    def __str__(self):
        return self.name


class Limitation(BaseModel):
    """
    Limitation class model.
    It provides ``from_age`` and ``to_age`` fields.
    """

    from_age = models.PositiveSmallIntegerField(
        verbose_name='Возраст',
        )
    to_age = models.PositiveSmallIntegerField(
        verbose_name='Возраст',
        )

    def __str__(self):
        return f'От {self.from_age}'
