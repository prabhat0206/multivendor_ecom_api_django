# Generated by Django 4.0.1 on 2022-08-05 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0011_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='description',
            field=models.TextField(default=''),
        ),
    ]