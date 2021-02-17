from django.db import models
from django.urls import reverse


class Schema(models.Model):
    """Represent schema model in database."""
    STATUS = (
        ('Creating', 'Creating'),
        ('Processing', 'Processing'),
        ('Ready', 'Ready')
    )
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True)
    created = models.DateField(auto_now_add=True, null=True)
    modified = models.DateField(auto_now=True, null=True)
    status = models.CharField(max_length=50, default='Creating', choices=STATUS)
    confirmed = models.BooleanField(default=False)

    class Meta:
        ordering = ['pk']

    def get_absolute_url(self):
        return reverse('schemas:schema_detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.name} {self.num_row}'


class Column(models.Model):
    """Represent schema column in database."""
    COLUMN_TYPES = (
        ('Full name', 'Full name'),
        ('Job', 'Job'),
        ('Company', 'Company'),
        ('Phone number', 'Phone number'),
        ('Integer', 'Integer')
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
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, null=True)
    num_row = models.SmallIntegerField()
    file = models.FileField(upload_to='data_sets/', null=True)

    def __str__(self):
        return f'{self.schema} - {self.num_row}'
