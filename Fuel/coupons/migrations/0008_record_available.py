# Generated by Django 5.0.6 on 2024-06-19 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0007_serviceissue_coupon_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='available',
            field=models.PositiveIntegerField(null=True),
        ),
    ]