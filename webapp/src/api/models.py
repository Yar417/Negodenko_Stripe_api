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


class Order(models.Model):
    """
    Order Django model
    """
    items = models.ManyToManyField(Item)

    def __str__(self):
        return f'Заказ #{self.pk}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Tax(models.Model):
    """
    Taxes Django model
    """
    name = models.CharField(max_length=200)
    rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'Налог #{self.pk}: {self.name}. Ставка: {self.rate}'

    class Meta:
        verbose_name = 'Налог'
        verbose_name_plural = 'Налоги'


class Discount(models.Model):
    """
    Discount Django model
    """
    name = models.CharField(max_length=200)
    rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'Скидка #{self.pk}: {self.name}. Ставка: {self.rate}%'

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'
