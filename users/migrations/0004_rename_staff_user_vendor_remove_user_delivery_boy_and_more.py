# Generated by Django 4.0.1 on 2022-06-07 06:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_address_ph_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='staff',
            new_name='vendor',
        ),
        migrations.RemoveField(
            model_name='user',
            name='delivery_boy',
        ),
        migrations.AddField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='last_otp_email',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='last_otp_ph_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=32, null=True, unique=True),
        ),
        migrations.CreateModel(
            name='VendorShop',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('vendor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
