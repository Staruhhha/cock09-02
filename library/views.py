from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from . import models as m

def home(request):
    return HttpResponse("<h1>Домашняя страница</h1>")

def all_books(request):
    books = m.Books.objects.all()
    page = "<h1>Книги: </h1>"

    for book in books:
        page += f"<a href = '/lib/books/{book.id}'>{book.name}</a>"

    return HttpResponse(page)

def id_book(request, id):
    book = get_object_or_404(m.Books, pk=id)
    page = "<h1>Книга: </h1>"
    page += f"<p>Название: {book.name} <p>"
    page += f"<p>Описание: {book.description} <p>"
    page += f"<p>Количество страниц: {book.count_pages} <p>"
    page += f"<p>Цена: {book.price} <p>"

    return HttpResponse(page)

def name_book(request, name):
    books = m.Books.objects.filter(name__contains=name)

    page = "<h1>Найденные книги: </h1>"

    for book in books:
        page += f"<p>{book.name}</p>"

    return HttpResponse(page)

def info(request):
    return render(request,'library/index.html')

def get_all_book(request):
    books = m.Books.objects.all()
    context = {
        'list': books
    }
    return render(request, 'library/query_all.html', context=context)

def get_one_book(request, id):
    book = get_object_or_404(m.Books, pk = id)
    return render(request, 'library/query_get.html', {'one_book': book})

def get_one_filter_book(request):
    find_books = m.Books.objects.filter(exists=request.GET.get('is_ex'))
    return render(request, 'library/query_filter.html', {'filter_books': find_books})

def get_more_filter_book(request):

    find_books = m.Books.objects.filter(
        price__lte=request.GET.get('max_price'),
        price__gt=request.GET.get('min_price')
    )
    return render(request,'library/query_filter.html', {'filter_books': find_books})

def get_one_by_one_filter_book(request):
    find_books = m.Books.objects.filter(price__lte=request.GET.get('max_price'))
    find_books = find_books.filter(name__contains=request.GET.get('name'))

    return render(request,'library/query_filter.html',{'filter_books': find_books})

def create_blank_book(request):
    new_book = m.Books()
    new_book.price = 10
    new_book.save()
    return render(request,'library/message.html', context={'message': 'Пустая книга была успешно создана'})

def create_book(request):
    new_book = m.Books()
    new_book.name = 'Ruby'
    new_book.price = 160
    new_book.count_pages = 120
    new_book.description = 'Описание по умолчанию'
    new_book.save()
    return render(request, 'library/message.html', context={'message': 'Книга была успешно создана'})

def create_user_book(request):
    name = request.GET.get('name')
    price = request.GET.get('price')
    count_pages = request.GET.get('count_pages')

    new_book = m.Books()
    new_book.name = name
    new_book.price = price
    new_book.count_pages = count_pages
    new_book.description = 'Описание по умолчанию'
    new_book.save()
    return render(request, 'library/message.html', context={'message': 'Книга с вашими параметрами была создана'})

def update_book(request, id):
    upd_book = get_object_or_404(m.Books, pk = id)
    upd_book.price = 1000
    upd_book.save()
    return render(request, 'library/message.html', context={'message': f'Книга с ID = {id} была успешно обновлена'})
def delete_book(request, id):
    del_book=get_object_or_404(m.Books, pk = id)
    del_book.delete()
    return render(request, 'library/message.html', context={'message': f'Книга с ID = {id} была успешно удалена'})