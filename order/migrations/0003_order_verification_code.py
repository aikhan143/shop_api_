# Generated by Django 5.0.2 on 2024-02-14 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_alter_cartproduct_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='verification_code',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
