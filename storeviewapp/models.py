from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from rest_framework.reverse import reverse
from unidecode import unidecode


# Create your models here.


class User(AbstractUser):
    avatar = models.ImageField(upload_to='media/users', blank=True)
    phone = models.CharField(max_length=20)
    brithday = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        indexes = (
            models.Index(fields=['username']),
            models.Index(fields=['first_name']),
            models.Index(fields=['last_name']),
            models.Index(fields=['email']),
        )


class TokenUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens')
    token = models.CharField(max_length=100, blank=True)


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('storeviewapp:category', kwargs={'slug': self.slug})


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('storeviewapp:manufacturer', kwargs={'slug': self.slug})


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField()
    stock = models.IntegerField()
    slug = models.CharField(max_length=100, unique=True, db_index=True, editable=False, blank=True)
    images = models.ManyToManyField('ProductImage', blank=True, related_name='images')
    monufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ('name',)
        verbose_name = 'product'
        verbose_name_plural = 'products'
        indexes = (
            models.Index(fields=['id'], name='id_index'),
            models.Index(fields=['name'], name='name_index'),
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('storeviewapp:product_detail', args=[self.slug, self.created_at.year, self.created_at.month,
                                                     self.created_at.day])


class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_images')