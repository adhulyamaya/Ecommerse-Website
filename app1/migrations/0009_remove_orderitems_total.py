# Generated by Django 4.1.7 on 2023-07-11 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0008_delete_banner_alter_orderitems_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitems',
            name='total',
        ),
    ]
