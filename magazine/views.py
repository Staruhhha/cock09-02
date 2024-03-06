from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator

from .models import *
from .forms import *
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'magazine/index.html')

def supplier_list(request):
    list_supplier = Supplier.objects.filter(is_exists=True)
    context = {
        'list_sup': list_supplier
    }
    return render(request, 'magazine/supplier/catalog.html', context)

def supplier_details(request, id):
    supplier = get_object_or_404(Supplier, pk = id)

    context = {
        'supplier_object': supplier
    }
    return render(request, 'magazine/supplier/details.html', context)
def supplier_create(request):
    if request.method == "POST":
        form_supplier = SupplierForm(request.POST)
        if form_supplier.is_valid():
            new_supplier = Supplier(**form_supplier.cleaned_data)
            new_supplier.save()
            messages.success(request, 'Поставщик успешно добавлен')
            return redirect('catalog_supplier_page')
        messages.error(request, 'Неверно заполнены поля')
    else:
        form_supplier = SupplierForm()
    context = {
        'form': form_supplier
    }
    return render(request, 'magazine/supplier/create.html', context)

def product_list(request):
    list_product = Product.objects.filter(exists=True)
    context = {
        'list_product': list_product
    }
    return render(request, 'magazine/product/catalog.html', context)


def product_delete(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('catalog_product_page')

# ----------------auth приложение-----------------------------


# Запись (login) пользователя в запрос (request) и удаление (logout) пользователя из запроса
from django.contrib.auth import login, logout

# Декораторы для проверки прав
# login_required - проверка авторизован ли пользователь
# permission_required - проверка прав у авторизированного пользователя
from django.contrib.auth.decorators import login_required, permission_required

# добавить прав к пользователю будет проще всего в админке
# но можно и с помощью кода это сделать

# Стандартная форма для регистрации пользователя и для аутентификации
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Собственная форма регистрации и авторизации (см в forms.py)
from .forms import RegistrationForm, LoginForm


# Для создания новых пользовательских прав доступа загляните в models класса Order внутри класса Meta

# Ссылки на страницы регистрации, авторизации и выхода из аккаунта находятся в index.html (../index/)

# Создание пользователя
# Проверка пароля при регистрации проверяется в AUTH_PASSWORD_VALIDATORS
def user_registration(request):
    if request.method == "POST":
        # Собственная форма создания пользователя
        form = RegistrationForm(request.POST)

        # Стандартная форма создания пользователя
        # form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)

            # Можем сразу авторизовать пользователя после регистрации
            login(request, user)

            # Сообщение о выполнении
            messages.success(request, 'Вы успешно зарегистрировались')

            return redirect('home_page')

        # Сообщение об ошибке
        messages.error(request, 'Что-то пошло не так')
    else:
        form = RegistrationForm()
        # form = UserCreationForm()
    return render(request, 'magazine/auth/registration.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        # Собственная форма авторизации пользователя
        form = LoginForm(data=request.POST)

        # Стандартная форма авторизации пользователя
        # form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Проверка на авторизацию пользователя
            print('is_anon:', request.user.is_anonymous)
            print('is_auth:', request.user.is_authenticated)

            # Авторизация пользователя в request (там он и останется)
            login(request, user)

            # Проверка на авторизацию пользователя
            print('is_anon:', request.user.is_anonymous)
            print('is_auth:', request.user.is_authenticated)
            print(user)

            # Сообщение о выполнении
            messages.success(request, 'Вы успешно авторизовались')

            return redirect('home_page')

        # Сообщение об ошибке
        messages.error(request, 'Что-то пошло не так')
    else:
        form = LoginForm()
        # form = AuthenticationForm()
    return render(request, 'magazine/auth/login.html', {'form': form})


# Деавторизация пользователя
def user_logout(request):
    logout(request)
    # Сообщение об ошибке
    messages.warning(request, 'Вы вышли из аккаунта')
    return redirect('log in')


def anon(request):
    # Проверка
    print('is_active:', request.user.is_active)
    print('is_anonymous:', request.user.is_anonymous)
    print('is_authenticated:', request.user.is_authenticated)
    print('is_staff:', request.user.is_staff)
    print('is_superuser:', request.user.is_superuser)

    # при проверке доступа доступ указывается следующим образом
    # <приложение>.<право>_<модель>
    # Права: add, change, view, delete
    print('может добавлять поставщика?', request.user.has_perm('magazine.add_supplier'))
    print('может добавлять и изменять поставщика?',
          request.user.has_perms(['magazine.change_supplier', 'magazine.add_supplier']))
    print('может изменять адресс?', request.user.has_perm('magazine.change_address'))
    return render(request, 'magazine/test/anon.html')


# Проверка на уровне бекенда
# @login_required()

# Если пользователь анонимный, то его перебросит на страницу авторизации (по умолчанию ссылка /accounts/login/)
# Но с помощью login_url можно переопределить
# @login_required(login_url=reverse('log in'))
# Либо в settings сразу переопределить для всего проекта

@login_required()
def auth(request):
    return render(request, 'magazine/test/auth.html')


# Проверка прав доступа
@permission_required('magazine.add_supplier')
def can_add_supplier(request):
    return render(request, 'magazine/test/can_add_supplier.html')


@permission_required(['magazine.add_supplier', 'magazine.change_supplier'])
def can_add_change_supplier(request):
    return render(request, 'magazine/test/can_add_change_supplier.html')


@permission_required('magazine.change_address')
def can_change_address(request):
    return render(request, 'magazine/test/can_change_address.html')



def catalog_product(request):
    many_prod = Product.objects.filter(exists=True)

    # Заполнение формы данными
    if request.GET != None:
        prod_form = ProductFilterForm(request.GET)
    else:
        prod_form = ProductFilterForm()

    # Проверка заполненности данными
    if prod_form.is_valid():

        print(prod_form.cleaned_data)

        if prod_form.cleaned_data.get('name') != "":  # строки имеют "" но не пустоту
            many_prod = many_prod.filter(name__contains=prod_form.cleaned_data.get('name'))

        if prod_form.cleaned_data.get('max_price'):
            many_prod = many_prod.filter(price__lte=prod_form.cleaned_data.get('max_price'))

        if prod_form.cleaned_data.get('min_price'):
            many_prod = many_prod.filter(price__gte=prod_form.cleaned_data.get('min_price'))

    context = {
        'list_object': many_prod,
        'form': prod_form,
    }

    return render(request, 'magazine/product/catalog.html', context)


# Вывод связанных данных с товаром
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product
    }
    return render(request, 'magazine/product/detail.html', context)


@permission_required('magazine.add_product')
def product_create(request):
    if request.method == "POST":
        form_prod = ProductForm(request.POST, request.FILES)
        if form_prod.is_valid():
            form_prod.save()
            messages.success(request, 'Продукт успешно добавлен')
            return redirect('catalog_product_page')

        messages.error(request, 'Неверно заполнены поля')
    else:
        form_prod = ProductForm()

    context = {
        'form': form_prod
    }
    return render(request, 'magazine/product/create.html', context)


@login_required()
def buy_product(request, pk):
    prod = Product.objects.get(pk=pk)
    messages.success(request, f'Товар {prod.name} успешно приобретен')
    return redirect('catalog_product_page')

@permission_required('magazine.add_supplier')
def supplier_create(request):
    if request.method == "POST":
        form_supplier = SupplierForm(request.POST)
        if form_supplier.is_valid():
            form_supplier.save()

            messages.success(request, 'Товар успешно добавлен')

            return redirect('catalog_product_page')

        messages.error(request, 'Неверно заполнены поля')
    else:
        form_supplier = SupplierForm()

    context = {
        'form': form_supplier
    }
    return render(request, 'magazine/supplier/create.html', context)

# _________________________________________________Generic___________________________________________
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class CategoryList(ListView):
    model = Category
    # по умолчанию название_приложения/название_модели + _list.html
    template_name = 'magazine/category/category_list.html'
    extra_context = {
        'title': 'Список книг из класса'
    }
    allow_empty = True

    # paginate_by = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Category.objects.all()

class CategoryDetail(DetailView):
    model = Category
    # по умолчанию название_приложения/название_модели + _detail.html

    template_name = 'magazine/category/category_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CategoryCreate(CreateView):
    model = Category

    form_class = CategoryForm

    extra_context = {
        'action': 'Создать',
    }
    # по умолчанию название_приложения/название_модели + _form.html
    template_name = 'magazine/category/category_form.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class CategoryUpdate(UpdateView):
    model =  Category
    form_class = CategoryForm

    extra_context = {
        'action': 'Изменить',
    }
    # по умолчанию название_приложения/название_модели + _form.html
    template_name = 'magazine/category/category_form.html'

    @method_decorator(permission_required('magazine.add_product'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class CategoryDelete(DeleteView):
    model = Category

    # (по умолчанию 'magazine/category_form.html') также как и при добавлении
    # (по умолчанию '<название приложения>/<название_модели>_form.html>')template_name = 'book/books/books-update.html'
    template_name = 'magazine/category/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')

    @method_decorator(permission_required('book.delete_books'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProductList(ListView):
    model = Product

    template_name = 'magazine/product/product_list.html'

    extra_context = {
        'title': 'Список товара'
    }
    allow_empty = True

    paginate_by = 3
    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return Product.objects.all()

class OrderList(ListView):
    model = Order
    template_name = 'magazine/order/order_list.html'

    @method_decorator(permission_required('magazine.view_order'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, args,kwargs)


class OrderDetail(DetailView):
    model = Order
    template_name = 'magazine/order/order_detail.html'

    @method_decorator(permission_required('magazine.view_order'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, args, kwargs)

class OrderCreate(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'magazine/order/order_form.html'
    extra_context = {
        'action': 'Создание',
        'action_button': 'Создать',
    }

    @method_decorator(permission_required('magazine.add_order'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, args, kwargs)


class OrderUpdate(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'magazine/order/order_form.html'
    extra_context = {
        'action': 'Изменение',
        'action_button': 'Изменить'
    }

    @method_decorator(permission_required('magazine.change_order'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class OrderDelete(DeleteView):
    model = Order
    template_name = 'magazine/order/order_delete.html'
    success_url = reverse_lazy('order_list')

    @method_decorator(permission_required('magazine.delete_order'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)



from django.http import JsonResponse
from .serializers import *

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets

def test_json(request):
    return JsonResponse({
        'message': 'Этот текс в формате JSON',
        'api_test': reverse_lazy('api_test'),
        'order_api_list': reverse_lazy('api_order_list'),
        'order_api_detail': reverse_lazy('api_order_detail', kwargs={'pk':1}),
        'product_api_viewset': '/magazine/api/products/',
    })


@api_view(['GET', 'POST'])
def api_order_list(request, format= None):
    if request.method == 'GET':
        order_list = Order.objects.all()
        serializer = OrderSerializer(order_list, many=True)
        print(serializer.data)
        return Response({'orders': serializer.data})
    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def order_api_detail(request, pk, format=None):
    obj = get_object_or_404(Order, pk=pk)
    if obj:
        if request.method == 'GET':
            serializer = OrderSerializer(obj)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = OrderSerializer(obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Данные успешно обновлены', 'order': serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(exists=True)
    serializer_class = ProductSerializer



#----------------------------------------ПЗ_1---------------------------------
