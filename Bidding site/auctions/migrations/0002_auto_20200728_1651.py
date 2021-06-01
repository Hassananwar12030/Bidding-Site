# Generated by Django 3.0.8 on 2020-07-28 11:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='list_item',
            old_name='discription',
            new_name='description',
        ),
        migrations.AlterField(
            model_name='list_item',
            name='item_creater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
