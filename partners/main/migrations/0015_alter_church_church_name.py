# Generated by Django 4.2.6 on 2023-10-21 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_alter_targetindividual_frequency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='church',
            name='church_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
