# Generated by Django 4.2.6 on 2023-10-16 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_patnershiparm_targetindividual_arm_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='main_target',
            field=models.IntegerField(null=True),
        ),
    ]
