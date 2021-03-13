import csv
import os
import random
import time

from django.core.files import File
from FakeCSV.celery import app
from faker import Faker

from .models import Column, DataSet


def get_fake_data(column):
    """
    Get fake data according to column type.
    """
    values = {
        'Full name': 'name',
        'Color': 'color',
        'City': 'city',
        'Company': 'company',
        'Phone number': 'phone_number',
        'Integer': 'integer',
        'Country': 'country',
        'Month': 'month'
    }
    value = values.get(column.type)

    if value == 'integer':
        return random.randint(column.start, column.end+1)

    else:
        return getattr(Faker(), value)()


@app.task
def form_fake_data(schema_id, dataset_id):
    """
    Form csv file with fake data according to schema column types.
    """
    data_set = DataSet.objects.get(pk=dataset_id)
    columns = Column.objects.filter(schema_id=schema_id)

    file_name = f'fake_data{schema_id}{dataset_id}.csv'
    file_path = os.path.join('media', 'temp', file_name)

    with open(file_path, 'w') as file:
        writer = csv.writer(file, delimiter=',')

        writer.writerow(
            [column.name for column in columns]
        )
        for row in range(data_set.num_row):
            writer.writerow(
                [get_fake_data(column) for column in columns]
            )

    with open(file_path, 'r') as file:
        data_set.file.save(file_name, File(file), save=False)
    data_set.status = 'Ready'
    data_set.save()

    return os.remove(file_path)
