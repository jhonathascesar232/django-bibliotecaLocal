# Generated by Django 3.1.4 on 2021-01-07 21:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0002_instancialivro_borrower'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='instancialivro',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', 'Set book as returned'),)},
        ),
    ]