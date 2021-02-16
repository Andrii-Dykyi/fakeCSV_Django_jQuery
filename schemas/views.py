from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, TemplateView, View
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import SchemaColumnForm, SchemaCreateForm
from .models import Schema, SchemaColumn
from .serializers import SchemaColumnSerializer


class IndexView(ListView):
    queryset = Schema.objects.filter(confirmed=True)
    context_object_name = 'schemas'
    template_name = 'schemas/index.html'


class CreateSchemaView(View):

    def get(self, request):
        schema, _ = Schema.objects.get_or_create(owner=request.user, confirmed=False)
        columns = schema.schemacolumn_set.all()
        form, col_form = SchemaCreateForm(instance=schema), SchemaColumnForm()
        context = {'schema': schema, 'columns': columns, 'form': form, 'col_form': col_form}
        return render(request, 'schemas/new_schema.html', context)


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
