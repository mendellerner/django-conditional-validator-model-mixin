from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .models_custom import ConditionalValidatorMixin
from django.utils.translation import gettext_lazy as _

conditional_schema_example = {
    'fauna': {
        'error_message_field_name': "Fauna",
        'field_values': {
            'a': {
                'error_message_field_value': "Animal",
                'include':['num_legs',],
                'exclude':['depth',],
            },
            'f': {
                'error_message_field_value': "Fish",
                'include':['depth',],
                'exclude':['num_legs',],
            },
        }}}

# Create your models here.
class Example(ConditionalValidatorMixin):
    conditional_schema = conditional_schema_example
    class Choices(models.TextChoices):
        BLANK = '', _('')
        ANIMAL = 'a', _('Animal')
        FISH = 'f', _('Fish')
        
    fauna = models.CharField(max_length=1, choices=Choices.choices, default=Choices.BLANK)
    num_legs = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    depth = models.IntegerField(blank=True, null=True, validators=[MaxValueValidator(0)])