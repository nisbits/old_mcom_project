# Generated by Django 4.1.3 on 2023-01-01 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trend', '0020_dpr_table1_mapa_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dpr_table1',
            name='MAPA_STATUS',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]