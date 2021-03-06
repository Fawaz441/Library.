# Generated by Django 4.0.5 on 2022-06-06 09:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_author_remove_book_author_book_authors'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='books.book')),
            ],
        ),
    ]
