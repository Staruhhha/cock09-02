from django.db import models

MAX_LENGTH_CHAR = 255


# Create your models here.
class Books(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название книги')
    description = models.TextField(blank=True, null=True, verbose_name='Описание книги')
    count_pages = models.IntegerField(null=True, verbose_name='Количество страниц')
    price = models.FloatField(verbose_name='Цена')
    release_date = models.DateField(auto_now_add=True, verbose_name='Дата издания')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')
    update_date = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения записи')
    photo = models.ImageField(upload_to='image/%Y/%m/%d', null=True, verbose_name='Фотография книги')
    exists = models.BooleanField(default=True, verbose_name='Выпущена?')

    publisher = models.ForeignKey('Publishing_house', on_delete=models.PROTECT, null=True, verbose_name='Издатель')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['name', '-price']


class Publishing_house(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    agent_firstname = models.CharField(max_length=50, verbose_name='Фамилия представителя')
    agent_name = models.CharField(max_length=50, verbose_name='Имя представителя')
    agent_patronymic = models.CharField(max_length=50, null=True, verbose_name='Отчество представителя')
    agent_telephone = models.CharField(max_length=20, null=True, verbose_name='Телефон представителя')

    def __str__(self):
        return self.title + " " + self.agent_firstname + ": " + self.agent_telephone

    class Meta:
        verbose_name = 'Издатель'
        verbose_name_plural = 'Издатели'


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название категории')
    description = models.TextField(verbose_name='Описание категории')

    books = models.ManyToManyField(Books)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Passport_book(models.Model):
    article = models.IntegerField(verbose_name='Артикль')
    features = models.CharField(max_length=255, verbose_name='Свойства книги')

    book = models.OneToOneField(Books, on_delete=models.PROTECT, primary_key=True, verbose_name='Книга')

    def __str__(self):
        return str(self.article) + " | " + self.book.__str__()

    class Meta:
        verbose_name = 'Паспорт книги'
        verbose_name_plural = 'Паспорт книг'