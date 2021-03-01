from django.urls import path

from . import views


app_name = 'schemas'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('new/schema/', views.CreateSchemaView.as_view(), name='create_schema'),
    path('new/column/', views.ColumnCreateView.as_view(), name='create_column'),
    path('column/delete/<int:column_id>/', views.ColumnDeleteView.as_view(), name='delete_column'),
    path('schema/<int:schema_id>/', views.SchemaView.as_view(), name='schema_detail'),
    path('schema/delete/<int:schema_id>', views.DeleteSchemaView.as_view(), name='delete_schema'),
    path('schema/get_file/<int:dataset_id>/', views.FileDownloadView.as_view(), name='get_file'),
    path('tasks/<str:task_id>/', views.TaskStatusView.as_view(), name='task_status')
]