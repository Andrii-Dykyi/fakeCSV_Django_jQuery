from celery.result import AsyncResult
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import View

from .forms import ColumnCreateForm, DataSetCreateForm, SchemaCreateForm
from .models import Column, DataSet, Schema
from .tasks import form_fake_data


def register_user(request):
    """
    Display registation form, create new user and if success redirect to index page.
    """
    if request.method == "GET":
        return render(request, 'registration/register.html')

    elif request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('schemas:index'))


class IndexView(LoginRequiredMixin, View):
    """
    Responsible for index page. Display all user's schemas.
    """
    def get(self, request):
        schemas = Schema.objects.filter(confirmed=True)
        return render(request, 'schemas/index.html', {'schemas': schemas})


class CreateSchemaView(LoginRequiredMixin, View):
    """
    Responsible for schema and columns creation page.
    Display forms and newly create columns.
    """
    def get(self, request):
        schema, _ = Schema.objects.get_or_create(owner=request.user, confirmed=False)
        columns = schema.column_set.all()
        form, col_form = SchemaCreateForm(instance=schema), ColumnCreateForm()
        context = {'schema': schema, 'columns': columns, 'form': form, 'col_form': col_form}
        return render(request, 'schemas/new_schema.html', context)

    def post(self, request):
        form = SchemaCreateForm(data=request.POST)

        if form.is_valid():
            schema = Schema.objects.get(owner=request.user, confirmed=False)
            schema.name = form.cleaned_data['name']
            schema.confirmed = True
            schema.save()
            return redirect(schema)


class ColumnCreateView(LoginRequiredMixin, View):
    """
    Responsible for column creation. Receive a POST AJAX request,
    create new column model in database and send json data to front end.
    """
    def post(self, request):
        if request.is_ajax():
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


class ColumnDeleteView(LoginRequiredMixin, View):
    """
    Responsible for column removal. Receive a POST AJAX request,
    remove column from database and send json data to front end.
    """
    def post(self, request, column_id):
        if request.is_ajax():
            column = Column.objects.filter(id=column_id)
            column.delete()
            return JsonResponse({'success': column_id}, status=202)

        else:
            return HttpResponseForbidden(status=403)


class DeleteSchemaView(LoginRequiredMixin, View):
    """
    Responsible for delete schemas. Receive a POST AJAX request
    and delete schema in database and send json data to front end.
    """
    def post(self, request, schema_id):
        if request.is_ajax():
            schema = Schema.objects.filter(id=schema_id, owner=request.user)
            schema.delete()
            return JsonResponse({'succsess': schema_id}, status=200)


class SchemaView(LoginRequiredMixin, View):
    """
    Responsible for schema detail and related datasets page.
    Display datasets table and create dataset form.
    Receive a POST AJAX request, create new dataset model,
    start Celery task to form CSV file and send json data to front end.
    """
    def get(self, request, schema_id):
        schema = get_object_or_404(Schema, pk=schema_id)
        data_sets = schema.dataset_set.all()
        form = DataSetCreateForm()
        context = {'schema': schema, 'data_sets': data_sets, 'form': form}
        return render(request, 'schemas/schema_detail.html', context)

    def post(self, request, schema_id):
        if request.is_ajax():
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
                    'dataset_id': data_set.id,
                    'created': data_set.created,
                    'status': data_set.status
                }

                return JsonResponse(response, status=202)

        else:
            return HttpResponseForbidden(status=403)


class TaskStatusView(LoginRequiredMixin, View):
    """
    Realize Celery task status polling.
    Recieve a GET AJAX request, check task status and send json data to front end.
    """
    def get(self, request, task_id):
        if request.is_ajax():
            task_result = AsyncResult(task_id)
            result = {
                "task_id": task_id,
                "task_status": task_result.status
            }
            return JsonResponse(result, status=202)

        else:
            return HttpResponseForbidden(status=403)


class FileDownloadView(LoginRequiredMixin, View):
    """
    Response for downloading file.
    """
    def get(self, request, dataset_id):
        data_set = get_object_or_404(DataSet, id=dataset_id)
        return FileResponse(open(data_set.file.path, 'rb'))
