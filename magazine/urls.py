from django.urls import path, include
from .views import *

urlpatterns = [
    path('index/',home, name='home_page' ),


    path('catalog/', catalog_product, name='catalog_product_page'),
    path('product/<int:pk>/', product_detail, name='product_detail_page'),
    path('product/create/', product_create, name='create_product_page'),
    path('product_delete/<int:id>', product_delete, name='delete_product'),
    path('product/buy/<int:pk>/', buy_product, name='buy_product_page'),

    path('suppliers/', supplier_list, name='catalog_suppliers_page'),
    path('suppliers/create/', supplier_create, name='add'),
    path('suppliers/changeadd/', can_add_change_supplier, name='add_change'),
    path('suppliers/address/', can_change_address, name='change_address'),
    path('suppliers/detail/<int:pk>/', supplier_details, name='detail_suppliers_page'),

    path('registration/', user_registration, name='regis'),
    path('login/', user_login, name='log in'),
    path('logout/', user_logout, name='log out'),


    path('anon/', anon, name='anon'),
    path('auth/', auth, name='auth'),

    path('category/', CategoryList.as_view(), name='category_list'),
    path('category/create', CategoryCreate.as_view(), name='category_create'),
    path('category/<int:pk>/detail/', CategoryDetail.as_view(), name='category_detail'),
    path('category/<int:pk>/update/', CategoryUpdate.as_view(), name='category_update'),

    path('catagory/<int:pk>/delete/', CategoryDelete.as_view(), name='category_delete'),

    path('product_list/', ProductList.as_view(), name='product_list'),

    path('order/', OrderList.as_view(), name='order_list'),
    path('order/<int:pk>/', OrderDetail.as_view(), name='order_detail'),
    path('order/create/', OrderCreate.as_view(), name='order_create'),
    path('order/update/<int:pk>', OrderUpdate.as_view(), name='order_update'),
    path('order/delete/<int:pk>', OrderDelete.as_view(), name='order_delete'),


    path('api/order/', api_order_list, name='api_order_list'),
    path('api/order/<int:pk>/', order_api_detail, name='api_order_detail')


]


from rest_framework import routers
router = routers.SimpleRouter()
router.register(r'api/products', ProductViewSet, basename='product')
urlpatterns += router.urls

