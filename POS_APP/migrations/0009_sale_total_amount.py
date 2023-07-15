# Generated by Django 4.2.2 on 2023-07-14 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POS_APP', '0008_remove_sale_total_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]