"""
URL configuration for shop_restapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework import routers
from django.urls import path, include

from storeviewapp.views import UserRestView, ProductRestView, CategoryRestView, ProductsDetailView, ManufacturerRestView
from rest_framework.authtoken.views import obtain_auth_token


app_name = 'storeviewapp'


router = routers.DefaultRouter()
router.register(r'users', UserRestView, basename='users')
router.register(r'categories', CategoryRestView, basename='categories')
router.register(r'manufacturer', ManufacturerRestView, basename='manufacturer')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/products/', ProductRestView.as_view(), name='products'),
    path('api/products/<str:slug>/', ProductRestView.as_view(), name='category_products'),
    path('api/products/monufactures/<str:monufactors>/', ProductRestView.as_view(), name='monufacturer_products'),
    path('api/products/filters/<str:slug>/<str:monufactors>/', ProductRestView.as_view(), name='filters_products'),
    path('api/products/path/<int:pk>/', ProductRestView.as_view(), name='path_product'),
    path('api/products/<str:slug>/<int:year>/<int:month>/<int:day>/', ProductsDetailView.as_view(), name='product_detail'),
]

