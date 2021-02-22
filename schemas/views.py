from celery.result import AsyncResult
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View

from .forms import ColumnCreateForm, DataSetCreateForm, SchemaCreateForm
from .models import Column, DataSet, Schema
from .tasks import form_fake_data


class IndexView(View):
    
    def get(self, request):
        if request.user.is_authenticated:
            schemas = Schema.objects.filter(confirmed=True)
            return render(request, 'schemas/index.html', {'schemas': schemas})

        else:
            return HttpResponseForbidden(status=403)


class CreateSchemaView(View):

    def get(self, request):
        if request.user.is_authenticated:
            schema, _ = Schema.objects.get_or_create(owner=request.user, confirmed=False)
            columns = schema.column_set.all()
            form, col_form = SchemaCreateForm(instance=schema), ColumnCreateForm()
            context = {'schema': schema, 'columns': columns, 'form': form, 'col_form': col_form}
            return render(request, 'schemas/new_schema.html', context)

        else:
            return HttpResponseForbidden(status=403)
    
    def post(self, request):
        if request.user.is_authenticated:
            form = SchemaCreateForm(data=request.POST)
            if form.is_valid():
                schema = Schema.objects.get(owner=request.user, confirmed=False)
                schema.name = form.cleaned_data['name']
                schema.confirmed = True
                schema.save()
                return redirect(schema)

        else:
            return HttpResponseForbidden(status=403)


class SchemaView(View):

    def get(self, request, schema_id):
        if request.user.is_authenticated:
            schema = get_object_or_404(Schema, pk=schema_id)
            data_sets = schema.dataset_set.all()
            form = DataSetCreateForm()
            context = {'schema': schema, 'data_sets': data_sets, 'form': form}
            return render(request, 'schemas/schema_detail.html', context)

    def post(self, request, schema_id):
        if request.is_ajax() and request.user.is_authenticated:
            schema = Schema.objects.get(id=schema_id)
            form = DataSetCreateForm(data=request.POST)

            if form.is_valid():
                data_set = DataSet.objects.create(
                    schema_id=schema_id,
                    num_row=request.POST.get('num_row')
                )
                task = form_fake_data.delay(schema_id, data_set.id)

                response = {
                    'task_id': task.id,
                    'count': schema.dataset_set.count(),
                    'created': data_set.created,
                    'status': data_set.status
                }

                return JsonResponse(response, status=202)

        else:
            return HttpResponseForbidden(status=403)


class ColumnCreateView(View):

    def post(self, request):
        if request.is_ajax() and request.user.is_authenticated:
            form = ColumnCreateForm(data=request.POST)
            if form.is_valid():
                column = form.save(commit=False)
                column.schema_id = request.POST.get('schema')
                column.save()
                response = {
                    'csrfmiddlewaretoken': request.POST.get('csrfmiddlewaretoken'),
                    'id': column.pk,
                    'name': column.name,
                    'type': column.type,
                    'start': column.start,
                    'end': column.end
                }
                return JsonResponse(response, status=202)

        else:
            return HttpResponseForbidden(status=403)


class ColumnDeleteView(View):

    def post(self, request, column_id):
        if request.is_ajax() and request.user.is_authenticated:
            column = Column.objects.filter(id=column_id)
            column.delete()
            return JsonResponse({'success': column_id}, status=202)


class TaskStatusView(View):

    def get(self, request, task_id):
        if request.is_ajax() and request.user.is_authenticated:
            task_result = AsyncResult(task_id)
            result = {
                "task_id": task_id,
                "task_status": task_result.status
            }
            return JsonResponse(result, status=202)

        else:
            return HttpResponseForbidden(status=403)
