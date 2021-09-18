# Generated by Django 3.2.7 on 2021-09-16 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('milk_CRM', '0003_alter_milk_transaction_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='milk_transaction',
            name='value',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='milk_transaction',
            name='customer',
            field=models.CharField(choices=[('Himanshu', 'Himanshu'), ('check', 'check'), ('check1', 'check1'), ('2nd element', '2nd element'), ('latest', 'latest')], max_length=20),
        ),
    ]
