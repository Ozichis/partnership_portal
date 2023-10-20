# Generated by Django 4.2.6 on 2023-10-19 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_user_church_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='church',
            old_name='user',
            new_name='userinfo',
        ),
        migrations.AddField(
            model_name='individual',
            name='church',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.church'),
        ),
        migrations.AddField(
            model_name='user',
            name='current_church',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.church'),
        ),
    ]
