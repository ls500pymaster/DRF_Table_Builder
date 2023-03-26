from django.db import models
from django.apps import apps
from django.core.exceptions import ValidationError
import re


def validate_table_name(table_name):
    if not re.match(r'^\w+$', table_name):
        raise ValidationError('Invalid table name. Table name must contain only alphanumeric characters and underscores.')


def create_dynamic_model(table_name, fields):
    validate_table_name(table_name)
    app_label = 'dynamic_tables'
    model_name = f'DynamicModel{table_name}'

    if apps.is_installed(app_label) and model_name in apps.all_models[app_label]:
        raise ValueError(f"A model with the name {table_name} already exists.")

    attrs = {
        '__module__': f'{app_label}.models',
        'Meta': type('Meta', (), {'db_table': table_name}),
    }

    for field_name, field_type in fields.items():
        if field_type == 'CharField':
            attrs[field_name] = models.CharField(max_length=255)
        elif field_type == 'IntegerField':
            attrs[field_name] = models.IntegerField()
        elif field_type == 'TextField':
            attrs[field_name] = models.TextField()
        elif field_type == 'BooleanField':
            attrs[field_name] = models.BooleanField()
        elif field_type == 'DateField':
            attrs[field_name] = models.DateField()
        elif field_type == 'DateTimeField':
            attrs[field_name] = models.DateTimeField()
        elif field_type == 'FloatField':
            attrs[field_name] = models.FloatField()
        elif field_type == 'DecimalField':
            attrs[field_name] = models.DecimalField(max_digits=10, decimal_places=2)
        else:
            raise ValueError(f"Unsupported field type: {field_type}")

    dynamic_model = type(model_name, (models.Model,), attrs)
    dynamic_model._meta.app_label = app_label
    dynamic_model._meta.db_table = table_name

    return dynamic_model

def get_dynamic_model(table_name):
    validate_table_name(table_name)
    app_label = 'dynamic_tables'
    model_name = f'DynamicModel{table_name}'

    if apps.is_installed(app_label) and model_name in apps.all_models[app_label]:
        return apps.get_model(app_label, model_name)
    else:
        raise ValueError(f"No model found with the name {table_name}.")
