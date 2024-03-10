from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView, GenericAPIView, CreateAPIView, ListCreateAPIView, UpdateAPIView
from .models import Product, Category, ProductImage, User, Manufacturer
from .serializer import ProductSerializer, CategorySerializer, UserSerializer, ManufacturerSerializer
from rest_framework.permissions import IsAuthenticated
from icecream import ic


# Create your views here.


class UserRestView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']


# class ProductRestView(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     http_method_names = ['get', 'post', 'patch', 'delete']


class ProductRestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, slug=None, monufactors=None):
        if slug:
            category = Category.objects.get(slug=slug)
            ic(category)
            product = Product.objects.filter(category=category)
            serializer = ProductSerializer(product, many=True)
            return Response(serializer.data)
        elif monufactors:
            manufacturer = Manufacturer.objects.get(slug=monufactors)
            product = Product.objects.filter(monufacturer=manufacturer)
            serializer = ProductSerializer(product, many=True)
            return Response(serializer.data)
        elif slug and monufactors:
            category = Category.objects.get(slug=slug)
            manufacturer = Manufacturer.objects.get(slug=monufactors)
            product = Product.objects.filter(category=category, monufacturer=manufacturer)
            serializer = ProductSerializer(product, many=True)
            return Response(serializer.data)
        else:
            product = Product.objects.all()
            serializer = ProductSerializer(product, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            images = request.FILES.getlist('images')
            product = Product.objects.create(
                name=data['name'],
                description=data['description'],
                category=Category.objects.get(id=data['category'].id),
                monufacturer=Manufacturer.objects.get(id=data['monufacturer'].id),
                price=data['price'],
                stock=data['stock'],
            )
            if images:
                for image in images:
                    images_instance = ProductImage.objects.create(image=image)
                    product.images.add(images_instance)
            serialized_product = ProductSerializer(product)
            return Response(serialized_product.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def patch(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryRestView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get', 'post', 'patch', 'delete']


class ManufacturerRestView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']


class ProductsDetailView(APIView):

    def get(self, request, slug, year, month, day):
        product = Product.objects.get(
            slug=str(slug),
        )
        serializer = ProductSerializer(product)
        return Response(serializer.data)