# Generated by Django 3.1.2 on 2020-12-02 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20201201_2326'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='win_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
