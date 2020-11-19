from collections import defaultdict
from django.core.exceptions import ValidationError
from django.db.models import Model
from django.utils.translation import gettext_lazy as _
from django.core.validators import EMPTY_VALUES

# Create your models here.
class ConditionalValidatorMixin(Model):
    """
    Checks conditional fields according to schema.\n
    Structure of schema is as follows:\n
    conditional_schema = {
        'field': { # Name of field that contains the controlling conditions.
            'error_message_field_name': "Field", # What you want to call the field in the validation message.
            'error_message_field_value': "Field Value", # What you want to call the field_value in the validation message.
            'field_values': { # Don't change this line.
                'field_value': { # Controlling field value to determine which fields to validate conditionally.
                    'include': ['conditional_field',], # Name the conditional fields here.
                    'exclude': ['conditional_field',], # Name the conditional fields here.
                }
            }
        }
    }
    IMPORTANT
    1. A non-specified 'field_value' will not check any fields.
    2. A 'conditional_field' not specified in 'include' or 'exclude' will not be checked for that specific field_value.
    """
    def __init__(self, *args, **kwargs):
        super(ConditionalValidatorMixin, self).__init__(*args, **kwargs)
        if not hasattr(self, 'conditional_schema'):
            e_text = """The 'conditional_schema' attribute must be defined in the model that calls ConditionalValidationMixin.\nFor example (in 'models.py'):\n\nclass Example(ConditionalValidationMixin):\n\t...\n\tconditional_schema = conditional_schema_example\n\t...\n\nSetting:\n\n\tconditional_schema = {}\n\nwill result in not validating any conditional fields, effectively making this mixin invisible."""
            raise AttributeError(e_text)
    
    def conditional_clean(self):
        """
        Conditional Cleaning function.
        """
        c_schema = self.conditional_schema
        e_array = defaultdict(list)
        for field in c_schema: # Iterate through rules for each field
            field_val = self.__getattribute__(field)
            if field_val in EMPTY_VALUES:
                return
            if not field_val in c_schema[field]['field_values']:
                return # No validation rules set

            e_str = lambda x: f'Field {x} when ' + c_schema[field]['error_message_field_name'] + ' = "' + c_schema[field]['field_values'][field_val]['error_message_field_value'] + '"'
            try:
                for f in c_schema[field]['field_values'][field_val]['include']:
                    if self.__getattribute__(f) in EMPTY_VALUES:
                        e_array[f].append(_(e_str('is required')))
                for f in c_schema[field]['field_values'][field_val]['exclude']:
                    if not self.__getattribute__(f) in EMPTY_VALUES:
                        e_array[f].append(_(e_str('must be empty')))
            except AttributeError:
                raise AttributeError
            if e_array != {}:
                raise ValidationError(e_array)

    def clean(self):
        self.conditional_clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)  # Call the "real" save() method.
    
    class Meta:
        abstract = True
