# Generated by Django 4.2.6 on 2023-10-16 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_individual_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='church_name',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
