from django.db import models


class Schema(models.Model):
    """Represent schema model in database."""
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True)
    num_row = models.PositiveIntegerField(null=True)
    created = models.DateField(auto_now_add=True, null=True)
    modified = models.DateField(auto_now=True, null=True)
    confirmed = models.BooleanField(default=False)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return f'{self.name} {self.num_row}'


class SchemaColumn(models.Model):
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
