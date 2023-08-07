# Generated by Django 4.1.3 on 2022-12-29 07:02

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trend', '0017_alter_performance_at_table_performance_at_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance_at_table',
            name='PERFORMANCE_AT_ACCEPTANCE_DATE',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(datetime.date(2022, 12, 29))]),
        ),
        migrations.AddField(
            model_name='performance_at_table',
            name='PERFORMANCE_AT_OFFERED_DATE',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(datetime.date(2022, 12, 29))]),
        ),
        migrations.AddField(
            model_name='performance_at_table',
            name='PERFORMANCE_AT_OFFERED_REMARKS',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='performance_at_table',
            name='PERFORMANCE_AT_PENDING_REASON',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='performance_at_table',
            name='PERFORMANCE_AT_PENDING_REMARK',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='performance_at_table',
            name='PERFORMANCE_AT_PENDING_TAT_DATE',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(datetime.date(2022, 12, 29))]),
        ),
        migrations.AddField(
            model_name='performance_at_table',
            name='PERFORMANCE_AT_REJECTED_TAT_DATE',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='performance_at_table',
            name='PERFORMANCE_AT_REJECTION_DATE',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(datetime.date(2022, 12, 29))]),
        ),
        migrations.AddField(
            model_name='performance_at_table',
            name='PERFORMANCE_AT_REJECTION_REASON',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dpr_table1',
            name='PERFORMANCE_AT_ACCEPTANCE_DATE',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(datetime.date(2022, 12, 29))]),
        ),
        migrations.AlterField(
            model_name='dpr_table1',
            name='PERFORMANCE_AT_OFFERED_DATE',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(datetime.date(2022, 12, 29))]),
        ),
        migrations.AlterField(
            model_name='dpr_table1',
            name='PERFORMANCE_AT_PENDING_TAT_DATE',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(datetime.date(2022, 12, 29))]),
        ),
        migrations.AlterField(
            model_name='dpr_table1',
            name='PERFORMANCE_AT_REJECTION_DATE',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(datetime.date(2022, 12, 29))]),
        ),
        migrations.AlterField(
            model_name='dpr_table1',
            name='PHYSICAL_AT_ACCEPTANCE_DATE',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(datetime.date(2022, 12, 29))]),
        ),
        migrations.AlterField(
            model_name='dpr_table1',
            name='PHYSICAL_AT_OFFERED_DATE',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(datetime.date(2022, 12, 29))]),
        ),
        migrations.AlterField(
            model_name='dpr_table1',
            name='PHYSICAL_AT_PENDING_TAT_DATE',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(datetime.date(2022, 12, 29))]),
        ),
        migrations.AlterField(
            model_name='dpr_table1',
            name='PHYSICAL_AT_REJECTED_TAT_DATE',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(datetime.date(2022, 12, 29))]),
        ),
        migrations.AlterField(
            model_name='dpr_table1',
            name='PHYSICAL_AT_REJECTION_DATE',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(datetime.date(2022, 12, 29))]),
        ),
        migrations.AlterField(
            model_name='dpr_table1',
            name='SOFT_AT_ACCEPTANCE_DATE',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(datetime.date(2022, 12, 29))]),
        ),
        migrations.AlterField(
            model_name='dpr_table1',
            name='SOFT_AT_OFFERED_DATE',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(datetime.date(2022, 12, 29))]),
        ),
        migrations.AlterField(
            model_name='dpr_table1',
            name='SOFT_AT_PENDING_TAT_DATE',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(datetime.date(2022, 12, 29))]),
        ),
        migrations.AlterField(
            model_name='dpr_table1',
            name='SOFT_AT_REJECTED_TAT_DATE',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(datetime.date(2022, 12, 29))]),
        ),
        migrations.AlterField(
            model_name='dpr_table1',
            name='SOFT_AT_REJECTION_DATE',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(datetime.date(2022, 12, 29))]),
        ),
    ]
