# Generated by Django 3.0.8 on 2020-07-31 04:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20200730_0118'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='itemName',
            new_name='item_id',
        ),
        migrations.RemoveField(
            model_name='bid',
            name='bid',
        ),
        migrations.AddField(
            model_name='bid',
            name='bid_id',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auctions.list_item'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='bidder',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
