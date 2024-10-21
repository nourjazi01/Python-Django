from django.db import models
from django.core.validators import RegexValidator
import re
from django.core.exceptions import ValidationError

def validate_letters_only(value):
    if not re.match(r'^[A-Za-z]+$',value):
        raise ValidationError('This field should only contain letters')

class category(models.Model):
    letters_only=RegexValidator(r'^$[A-Za-z]+','Only letters are allowed')
    title=models.CharField(max_length=255,validators=[validate_letters_only])
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural="categories"