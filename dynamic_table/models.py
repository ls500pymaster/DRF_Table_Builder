from django.db import models

from django.db import models

def create_dynamic_model(name, fields):
    """
    Create a new Django model with the given name and fields.

    :param name: The name of the new model.
    :param fields: A list of fields as (name, field_type, options) tuples.
    :return: The newly created model class.
    """
    attrs = {
        '__module__': __name__,
        'Meta': type('Meta', (), {'managed': True, 'verbose_name_plural': name}),
    }

    for field_name, field_type, field_options in fields:
        try:
            field_class = getattr(models, field_type)
        except AttributeError:
            raise ValueError(f"Invalid field type: {field_type}")

        attrs[field_name] = field_class(**field_options)

    return type(name, (models.Model,), attrs)

