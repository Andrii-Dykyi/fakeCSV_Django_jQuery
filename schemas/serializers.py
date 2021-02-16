from rest_framework import serializers

from .models import SchemaColumn


class SchemaColumnSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SchemaColumn
        fields = '__all__'
