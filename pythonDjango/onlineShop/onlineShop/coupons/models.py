from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from django.utils.translation import gettext_lazy as _

# Create your models here.
class Coupon(models.Model):
    code = models.CharField(_('code'), max_length=50, unique=True)
    valid_from = models.DateTimeField(_('valid from'),)
    valid_to = models.DateTimeField(_('valid to'),)
    discount = models.IntegerField(_('discount'), validators=[MinValueValidator(0), 
        MaxValueValidator(100)])
    active = models.BooleanField(_('active'), default=False)

    def __str__(self):
        return self.code
