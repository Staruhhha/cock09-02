from  django.urls import path, include
from . import views as v

urlpatterns = [
    path('index/', v.home),
    path('books/', v.all_books),
    path('books/<int:id>/', v.id_book),
    path('books/<str:name>/', v.name_book),
    path('', v.info),
    path('query/books/', v.get_all_book),
    path('query/books/<int:id>/', v.get_one_book),
    path('query/books/one-filter/', v.get_one_filter_book),
    path('query/books/more-filter/', v.get_more_filter_book),
    path('query/books/one-by-one-filter/', v.get_one_by_one_filter_book),
    path('query/books/create_blank/', v.create_blank_book),
    path('query/books/create/', v.create_book),
    path('query/books/create_user_book/', v.create_user_book),
    path('query/books/update/<int:id>/', v.update_book),
    path('query/books/delete/<int:id>/', v.delete_book),




]