# Generated by Django 4.0.5 on 2022-06-06 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0012_bookborrowrequest_book_returned'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
    ]