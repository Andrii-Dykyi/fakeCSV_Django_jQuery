from django.db import models
from django.urls import reverse


class Schema(models.Model):
    """Represent schema model in database."""
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True)
    modified = models.DateField(auto_now=True, null=True)
    confirmed = models.BooleanField(default=False)

    class Meta:
        ordering = ['pk']

    def get_absolute_url(self):
        return reverse('schemas:schema_detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.name}'


class Column(models.Model):
    """Represent schema column in database."""
    COLUMN_TYPES = (
        ('Full name', 'Full name'),
        ('Color', 'Color'),
        ('City', 'City'),
        ('Company', 'Company'),
        ('Phone_number', 'Phone number'),
        ('Integer', 'Integer'),
        ('Country', 'Country'),
        ('Month', 'Month')
    )
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=COLUMN_TYPES)
    start = models.PositiveSmallIntegerField(null=True, blank=True)
    end = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return f'{self.name} {self.type}'


class DataSet(models.Model):
    """Represent schema dataset in database."""
    STATUS = (
        ('Processing', 'Processing'),
        ('Ready', 'Ready')
    )
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, null=True)
    num_row = models.SmallIntegerField()
    status = models.CharField(max_length=50, default='Processing', choices=STATUS)
    created = models.DateField(auto_now_add=True, null=True)
    file = models.FileField(upload_to='data_sets/', null=True)

    def __str__(self):
        return f'{self.schema} - {self.num_row}'
