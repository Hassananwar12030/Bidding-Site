# Generated by Django 3.0.8 on 2020-07-28 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20200728_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list_item',
            name='picture_item',
            field=models.ImageField(upload_to=''),
        ),
    ]
