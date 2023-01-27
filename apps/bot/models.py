from django.db import models


class City(models.Model):
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


class Fund(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=256,
        help_text='Название фонда.',
        )
        
    def __str__(self):
        return self.name


class Limitation(models.Model):
    from_age = models.PositiveSmallIntegerField(
        verbose_name='Возраст',
        )
    to_age = models.PositiveSmallIntegerField(
        verbose_name='Возраст',
        )
        
    def __str__(self):
        return f'От {self.from_age}'
