from django.db import models
from django.urls import reverse_lazy

MAX_LENGTH_CHAR = 255

# Create your models here.
class Supplier(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Название компании')
    agent_firstname = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Фамилия представителя')
    agent_name = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Имя представителя')
    agent_patronymic = models.CharField(max_length=MAX_LENGTH_CHAR, null=True, verbose_name='Отчество представителя')
    agent_telephone = models.CharField(max_length=MAX_LENGTH_CHAR, null=True, verbose_name='Телефон представителя')
    address = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Адрес поставщика')
    is_exists = models.BooleanField(default=True, verbose_name='Логическое удаление')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

        # Добавление новых пользовательских прав доступа для таблицы
        permissions = [
            ('change_address', 'Возможность изменить адрес доставки'),
            ('can_del_supplier', 'Возможность удалить поставщика'),
        ]
        # После добавление новых разрешений, не забудьте провести миграцию python manage.py makemigrations/migrate
        # Т.к. нужно их добавить в таблицу permissions
        # Но учтите, остальные механизмы проверки и выполнения создаются вручную во view, здесь же просто добавление
        # нового вида доступа, но не механизма



class Supply(models.Model):
    data_supply = models.DateTimeField(verbose_name='Дата поставки')
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, verbose_name='Поставщик')

    product = models.ManyToManyField('Product', through='Pos_supply', verbose_name='Продукты')

    def __str__(self):
        return f'#{self.pk} - {self.data_supply} {self.supplier.name}'

    class Meta:
        verbose_name = 'Поставка'
        verbose_name_plural = 'Поставки'



class Parametr(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Название характеристики')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристика'

class Category(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def get_absolute_url(self):
        return reverse_lazy('category_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Tag(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name =  'Тег'
        verbose_name_plural = 'Теги'


class Order(models.Model):
    MAGAZINE = "MG"
    COURIER = "CR"
    PICKUPPOINT = "PP"
    TYPE_DELIVERY = [
        (MAGAZINE, "Магазин"),
        (COURIER, "Курьер"),
        (PICKUPPOINT, "Пункт выдачи"),
    ]
    FIO_customer = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='ФИО покупателя')
    comment = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Комментарий')
    delivery_address = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Адрес доставки')
    delivery_type = models.CharField(max_length=2, choices=TYPE_DELIVERY, default=MAGAZINE, verbose_name='Способ доставки')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')
    date_finish = models.DateTimeField(null=True, blank=True, verbose_name='Дата завершенияя заказа')

    books = models.ManyToManyField('Product', through='Pos_order', verbose_name='Товар')

    def get_absolute_url(self):
        return reverse_lazy('order_detail', kwargs={'pk':self.pk})
    def __str__(self):
        return f'{self.pk} {self.FIO_customer} {self.date_create}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

class Product(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Название товара')
    description = models.TextField(null=True, blank=True, verbose_name='Описание товара')
    price = models.FloatField(verbose_name='Цена')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')
    update_date = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления записи')
    photo = models.ImageField(upload_to='image/%Y/%m/%d', null=True,blank=True, verbose_name='Фотография товара')
    exists = models.BooleanField(default=True, verbose_name='В наличии?')

    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    tag = models.ManyToManyField(Tag, blank=True, verbose_name='Тег')
    parametr = models.ManyToManyField(Parametr, through='Pos_parametr', verbose_name='Характеристики')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Pos_parametr(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Продукт')
    parametr = models.ForeignKey(Parametr, on_delete=models.PROTECT, verbose_name='Характеристика')

    value = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Значение')

    def __str__(self):
        return f'{self.product.name} - {self.value}'

    class Meta:
        verbose_name = 'Позиция характеристики'
        verbose_name_plural = 'Позиции характеристик'


class Pos_supply(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Продукт')
    supply = models.ForeignKey(Supply,on_delete=models.PROTECT, verbose_name='Поставка' )

    count = models.PositiveIntegerField(verbose_name='Количество продукта')

    def __str__(self):
        return f'{self.product.name} - #{self.supply.pk}'

    class Meta:
        verbose_name = 'Позиция поставки'
        verbose_name_plural = 'Позиции поставок'

class Pos_order(models.Model):
    product = models.ForeignKey('Product', on_delete=models.PROTECT, verbose_name='Продукт')
    order = models.ForeignKey('Order', on_delete=models.PROTECT, verbose_name='Заказ')
    count = models.PositiveIntegerField(default=1, verbose_name='Количество продукта')
    discount = models.PositiveIntegerField(default=0, verbose_name='Скидка продукта')

    def __str__(self):
        return f"{self.pk} {self.product.name} {self.order.FIO_customer}"

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'