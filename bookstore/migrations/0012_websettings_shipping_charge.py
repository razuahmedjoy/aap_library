# Generated by Django 3.2 on 2022-04-27 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0011_auto_20220427_0115'),
    ]

    operations = [
        migrations.AddField(
            model_name='websettings',
            name='shipping_charge',
            field=models.IntegerField(default=50),
        ),
    ]