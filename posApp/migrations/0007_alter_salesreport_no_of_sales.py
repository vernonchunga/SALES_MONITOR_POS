# Generated by Django 4.2.2 on 2023-09-04 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posApp', '0006_rename_total_sales_salesreport_no_of_sales_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesreport',
            name='No_of_sales',
            field=models.IntegerField(default=0),
        ),
    ]