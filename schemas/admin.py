from django.contrib import admin

# Register your models here.
from .models import Schema, SchemaColumn


admin.site.register(Schema)
admin.site.register(SchemaColumn)
