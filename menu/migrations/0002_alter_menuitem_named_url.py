# Generated by Django 5.1 on 2024-09-03 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='named_url',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Named URL'),
        ),
    ]
