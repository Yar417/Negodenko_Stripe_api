from django.db import models


class Item(models.Model):
    '''
    Django Модель
    Item с полями (name, description, price)
    '''
    name = models.CharField('Название', max_length=250, null=False, blank=True)
    description = models.TextField('Описание', max_length=400, null=False, blank=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Товар #{self.pk}: {self.name}. Цена: {self.price}'
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'