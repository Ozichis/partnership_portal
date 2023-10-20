# Generated by Django 4.2.6 on 2023-10-15 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_church_patnership_targetchurch_targetindividual_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatnershipArm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
            ],
        ),
        migrations.AddField(
            model_name='targetindividual',
            name='arm',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.patnership'),
        ),
        migrations.AlterField(
            model_name='targetchurch',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='targetchurch',
            name='end_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='targetchurch',
            name='start_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='targetchurch',
            name='target_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='targetindividual',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='targetindividual',
            name='end_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='targetindividual',
            name='start_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='targetindividual',
            name='target_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='patnership',
            name='arm',
            field=models.ForeignKey(default=12, on_delete=django.db.models.deletion.CASCADE, to='main.patnershiparm'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='targetchurch',
            name='arm',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.patnershiparm'),
        ),
    ]