# Generated by Django 5.0.6 on 2024-06-19 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('fuel_type', models.CharField(choices=[('Diesel', 'Diesel'), ('Petrol', 'Petrol')], max_length=20)),
                ('serial_number_group', models.CharField(max_length=50, unique=True)),
                ('quantity', models.IntegerField(null=True)),
                ('supplier', models.CharField(choices=[('Redan', 'Redan'), ('Petrotrade', 'Petrotrade')], max_length=50)),
                ('purpose', models.CharField(choices=[('Condition of Service', 'Condition of Service'), ('Monthly Allocation', 'Monthly Allocation')], max_length=255, null=True)),
                ('amount_for_one', models.IntegerField(null=True)),
                ('amount_in_litres', models.IntegerField(editable=False, null=True)),
            ],
            options={
                'ordering': ['-creation_date'],
            },
        ),
    ]
