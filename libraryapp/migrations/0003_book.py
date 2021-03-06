# Generated by Django 3.0.6 on 2021-07-30 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0002_bookcategorie'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookname', models.CharField(max_length=150)),
                ('authorname', models.CharField(max_length=200)),
                ('isbnno', models.CharField(max_length=50)),
                ('quantity', models.IntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libraryapp.BookCategorie')),
            ],
        ),
    ]
