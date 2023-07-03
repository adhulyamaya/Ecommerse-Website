# Generated by Django 4.1.7 on 2023-06-26 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='Variant',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_image',
        ),
        migrations.AddField(
            model_name='variant',
            name='image1',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='variant',
            name='image2',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='variant',
            name='image3',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='variant',
            name='image4',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
        migrations.DeleteModel(
            name='Images',
        ),
    ]