from django.db import models

from django.urls import reverse

from parler.models import TranslatableModel, TranslatedFields

# Create your models here.
# class Category(models.Model):
class Category(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=200, db_index=True),
        slug = models.SlugField(max_length=200, db_index=True, unique=True)
    )

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

    class Meta:
        # You cannot include a translatable field in the ordering Meta options when using Parler
        # ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


# class Product(models.Model):
class Product(TranslatableModel):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.PROTECT)
    translations = TranslatedFields(
        name = models.CharField(max_length=200, db_index=True),
        slug = models.SlugField(max_length=200, db_index=True),
        description = models.TextField(blank=True)
    )
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    # Always use DecimalField to avoid float rounding issues
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

    class Meta:
        ordering = ('created',)
        # index_together is not supported in parler as well
        # index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name
