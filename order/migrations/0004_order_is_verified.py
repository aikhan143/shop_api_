# Generated by Django 5.0.2 on 2024-02-14 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_order_verification_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]