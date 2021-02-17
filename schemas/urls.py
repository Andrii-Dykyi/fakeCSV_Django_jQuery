from django.urls import path

from . import views


app_name = 'schemas'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('new_schema/', views.CreateSchemaView.as_view(), name='create_schema'),
    path('new_column/', views.ColumnCreateView.as_view(), name='create_column'),
    path('new_column/delete/<int:column_id>/', views.ColumnDeleteView.as_view(), name='delete_column'),
    path('schema/<int:schema_id>/', views.SchemaView.as_view(), name='schema_detail'),
]