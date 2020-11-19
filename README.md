# Conditional Field Validator for Django Models
A custom mixin for Django models to validate model fields according to the values in another field.

## Usage
Import `models_custom.py` into your `models.py` using:
```python
from .conditional_validator_mixin import ConditionalValidatorMixin
```
Use like any other model Mixin and add a `conditional_schema` property:
```python
class Example(ConditionalValidatorMixin):
    conditional_schema = conditional_schema_example
```

## Example Usage
`models.py`
```python
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .conditional_validator_mixin import ConditionalValidatorMixin
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
``` 

## Documentation Sources
1. [Django Models - Custom Validation](https://docs.djangoproject.com/en/3.1/ref/models/instances/#validating-objects)
2. [Django Enumeration Types](https://docs.djangoproject.com/en/3.1/ref/models/fields/#enumeration-types)

## Compatibility
Tested on `Django 3.0+`
