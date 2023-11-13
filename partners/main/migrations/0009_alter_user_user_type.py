# Generated by Django 4.2.6 on 2023-10-19 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_rename_user_church_userinfo_individual_church_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'church'), (2, 'individual'), (3, 'admin')], default=1),
        ),
    ]