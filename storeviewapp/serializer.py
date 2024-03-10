from rest_framework import serializers
from .models import Product, User, Category, ProductImage, Manufacturer
from icecream import ic

class CategoryChoiceField(serializers.RelatedField):
    def to_internal_value(self, data):
        try:
            return Category.objects.get(id=int(data))
        except (ValueError, Category.DoesNotExist):
            raise serializers.ValidationError('Invalid category id')

    def to_representation(self, obj):
        return obj.id


class ManufacturedChoiceField(serializers.RelatedField):
    def to_internal_value(self, data):
        try:
            return Manufacturer.objects.get(id=int(data))
        except (ValueError, Category.DoesNotExist):
            raise serializers.ValidationError('Invalid category id')

    def to_representation(self, obj):
        return obj.id


class ProductSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    category = CategoryChoiceField(queryset=Category.objects.all(), required=False)
    monufacturer = ManufacturedChoiceField(queryset=Manufacturer.objects.all(), required=False)
    price = serializers.FloatField()
    stock = serializers.IntegerField()
    images = serializers.FileField(max_length=None, use_url=True)
    slug = serializers.CharField(required=False, allow_blank=True)
    absolute_url = serializers.SerializerMethodField('get_absolute_url')

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            if field != 'images':  # Обрабатываем остальные поля без изменений
                setattr(instance, field, value)
        if 'images' in validated_data:
            image_data = validated_data.pop('images')
            image = ProductImage.objects.create(image=image_data)
            instance.images.add(image)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password')


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    slug = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = Category
        fields = '__all__'


class ManufacturerSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    slug = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Manufacturer
        fields = '__all__'