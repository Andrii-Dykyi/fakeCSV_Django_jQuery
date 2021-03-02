from django.contrib import admin

from .models import Schema, Column, DataSet


# Not customized admin panel, using just for debug.
admin.site.register(Schema)
admin.site.register(Column)
admin.site.register(DataSet)
