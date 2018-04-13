# Generated by Django 2.0.4 on 2018-04-12 17:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('portscan', '0009_auto_20180412_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scanitems',
            name='itemid',
            field=models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='任务编号'),
        ),
    ]
