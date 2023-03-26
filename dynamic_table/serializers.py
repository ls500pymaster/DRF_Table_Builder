from rest_framework import serializers
from django.core.exceptions import ValidationError
from .utils import create_dynamic_model, get_dynamic_model


class DynamicTableSerializer(serializers.Serializer):
    table_name = serializers.CharField(max_length=100)
    fields = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )

    def create(self, validated_data):
        table_name = validated_data['table_name']
        fields = validated_data['fields']

        try:
            model = create_dynamic_model(table_name, fields)
        except ValueError as e:
            raise ValidationError(str(e))

        return model
