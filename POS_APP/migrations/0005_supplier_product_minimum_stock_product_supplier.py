# Generated by Django 4.2.2 on 2023-07-12 21:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('POS_APP', '0004_alter_sale_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='minimum_stock',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='supplier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='POS_APP.supplier'),
        ),
    ]