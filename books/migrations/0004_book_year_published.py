# Generated by Django 4.0.5 on 2022-06-05 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_category_book_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='year_published',
            field=models.IntegerField(default=2020),
            preserve_default=False,
        ),
    ]
