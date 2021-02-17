from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, View
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import ColumnCreateForm, SchemaCreateForm, DataSetCreateForm
from .models import Schema, Column
from .serializers import ColumnSerializer


class IndexView(ListView):
    queryset = Schema.objects.filter(confirmed=True)
    context_object_name = 'schemas'
    template_name = 'schemas/index.html'


class CreateSchemaView(View):

    def get(self, request):
        if request.user.is_authenticated:
            schema, _ = Schema.objects.get_or_create(owner=request.user, confirmed=False)
            columns = schema.column_set.all()
            form, col_form = SchemaCreateForm(instance=schema), ColumnCreateForm()
            context = {'schema': schema, 'columns': columns, 'form': form, 'col_form': col_form}
            return render(request, 'schemas/new_schema.html', context)
    
    def post(self, request):
        if request.user.is_authenticated:
            form = SchemaCreateForm(data=request.POST)
            if form.is_valid():
                schema = form.save(commit=False)
                schema.confirmed = True
                schema.status = 'Processing'
                schema.save()
                return redirect('schemas:schema_detail')


class SchemaView(View):

    def get(self, request, schema_id):
        schema = get_object_or_404(Schema, pk=schema_id)
        form = DataSetCreateForm()
        return render(request, 'schemas/schema_detail.html', {'schema': schema, 'form': form})


class ColumnCreateView(APIView):

    def post(self, request):
        if request.is_ajax() and request.user.is_authenticated:
            serializer = SchemaColumnSerializer(data=request.POST)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)


class ColumnDeleteView(View):

    def get(self, request, column_id):
        if request.is_ajax() and request.user.is_authenticated:
            column = SchemaColumn.objects.filter(id=column_id)
            column.delete()
            return JsonResponse({'success': column_id}, status=202)
