# Generated by Django 4.2.2 on 2023-07-14 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('POS_APP', '0007_product_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='total_amount',
        ),
    ]
